import customtkinter as ctk
import requests as req
from plyer import notification
from integrations.vatsim import get_atc
from core.position import get_position
from core.logic import find_nearest_atc, should_alert
from core.settings import load, save
from ui.languages import LANGUAGES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

REFRESH_OPTIONS = {"30s": 30, "60s": 60, "120s": 120, "Off": 0}
NTFY_URL = "https://ntfy.sh"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        s = load()
        self.lang_code = s["lang_code"]
        self.alert_distance = s["alert_distance"]
        self.refresh_interval = s["refresh_interval"]
        self.theme = s["theme"]

        ctk.set_appearance_mode(self.theme)

        self.last_alerted = None
        self._refresh_job: str | None = None

        self.title("ATC Advisor")
        self.geometry("500x500")
        self.resizable(False, False)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabview.add("ATC")
        self.tabview.add("⚙")

        self._build_main_tab()
        self._build_settings_tab(s)

        self.refresh_atc()
        self._schedule_refresh()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def t(self, key: str) -> str:
        result = LANGUAGES[self.lang_code].get(key, key)
        return result if result is not None else key

    def _build_main_tab(self) -> None:
        tab = self.tabview.tab("ATC")

        self.title_label = ctk.CTkLabel(tab, text="ATC Advisor", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=(15, 5))

        self.info_label = ctk.CTkLabel(tab, text="", font=("Arial", 15))
        self.info_label.pack(pady=15)

        self.refresh_btn = ctk.CTkButton(tab, text=self.t("refresh"), command=self.refresh_atc)
        self.refresh_btn.pack(pady=5)

    def _build_settings_tab(self, s: dict) -> None:
        tab = self.tabview.tab("⚙")

        self.lang_label = ctk.CTkLabel(tab, text=self.t("language"), font=("Arial", 14))
        self.lang_label.pack(pady=(10, 2))

        self.lang_menu = ctk.CTkOptionMenu(
            tab,
            values=list(LANGUAGES.keys()),
            command=self._on_language_change
        )
        self.lang_menu.set(self.lang_code)
        self.lang_menu.pack(pady=5)

        self.theme_label = ctk.CTkLabel(tab, text=self.t("theme"), font=("Arial", 14))
        self.theme_label.pack(pady=(10, 2))

        self.theme_menu = ctk.CTkOptionMenu(
            tab,
            values=[
                self.t("theme_dark"),
                self.t("theme_light"),
                self.t("theme_system")
            ],
            command=self._on_theme_change
        )

        self.theme_menu.set(self.t(f"theme_{self.theme}"))
        self.theme_menu.pack(pady=5)

        self.dist_label = ctk.CTkLabel(tab, text=self.t("alert_distance"), font=("Arial", 14))
        self.dist_label.pack(pady=(10, 2))

        self.dist_slider = ctk.CTkSlider(
            tab,
            from_=10,
            to=200,
            number_of_steps=190,
            command=self._on_slider_change
        )
        self.dist_slider.set(self.alert_distance)
        self.dist_slider.pack(pady=5)

        self.dist_value_label = ctk.CTkLabel(tab, text=f"{self.alert_distance} NM", font=("Arial", 13))
        self.dist_value_label.pack()

        self.refresh_label = ctk.CTkLabel(tab, text=self.t("auto_refresh"), font=("Arial", 14))
        self.refresh_label.pack(pady=(10, 2))

        self.refresh_menu = ctk.CTkOptionMenu(
            tab,
            values=list(REFRESH_OPTIONS.keys()),
            command=self._on_refresh_change
        )

        refresh_key = next(
            (k for k, v in REFRESH_OPTIONS.items() if v == self.refresh_interval),
            "60s"
        )

        self.refresh_menu.set(refresh_key)
        self.refresh_menu.pack(pady=5)

        self.ntfy_label = ctk.CTkLabel(tab, text=self.t("ntfy_label"), font=("Arial", 14))
        self.ntfy_label.pack(pady=(10, 2))

        self.ntfy_entry = ctk.CTkEntry(tab, placeholder_text=self.t("ntfy_topic"), width=220)
        self.ntfy_entry.insert(0, s.get("ntfy_topic", ""))
        self.ntfy_entry.pack(pady=5)

    def _on_close(self) -> None:
        save({
            "lang_code": self.lang_code,
            "alert_distance": self.alert_distance,
            "refresh_interval": self.refresh_interval,
            "ntfy_topic": self.ntfy_entry.get().strip(),
            "theme": self.theme,
        })
        self.destroy()

    def _on_language_change(self, lang: str) -> None:
        self.lang_code = lang

        self.refresh_btn.configure(text=self.t("refresh"))
        self.lang_label.configure(text=self.t("language"))
        self.dist_label.configure(text=self.t("alert_distance"))
        self.refresh_label.configure(text=self.t("auto_refresh"))
        self.ntfy_label.configure(text=self.t("ntfy_label"))
        self.theme_label.configure(text=self.t("theme"))
        self.theme_menu.configure(
            values=[
                self.t("theme_dark"),
                self.t("theme_light"),
                self.t("theme_system"),
            ]
        )

        self.theme_menu.set(self.t(f"theme_{self.theme}"))

    def _on_theme_change(self, value: str) -> None:
        reverse = {
            self.t("theme_dark"): "dark",
            self.t("theme_light"): "light",
            self.t("theme_system"): "system",
        }

        theme = reverse.get(value, "system")
        self.theme = theme
        ctk.set_appearance_mode(theme)

    def _on_slider_change(self, value: float) -> None:
        self.alert_distance = int(value)
        self.dist_value_label.configure(text=f"{self.alert_distance} NM")

    def _on_refresh_change(self, option: str) -> None:
        self.refresh_interval = REFRESH_OPTIONS[option]

        if self._refresh_job is not None:
            self.after_cancel(self._refresh_job)
            self._refresh_job = None

        self._schedule_refresh()

    def _schedule_refresh(self) -> None:
        if self.refresh_interval > 0:
            self._refresh_job = self.after(
                self.refresh_interval * 1000,
                self._auto_refresh
            )

    def _auto_refresh(self) -> None:
        self.refresh_atc()
        self._schedule_refresh()

    def _send_ntfy(self, message: str) -> None:
        topic = self.ntfy_entry.get().strip()
        if not topic:
            return

        try:
            req.post(
                f"{NTFY_URL}/{topic}",
                data=message.encode("utf-8"),
                headers={"Title": "ATC Advisor"},
                timeout=5
            )
        except Exception as e:
            print("[NTFY ERROR]", e)

    def refresh_atc(self) -> None:
        pos = get_position()
        if pos is None:
            self.info_label.configure(text=self.t("no_position"))
            return

        atc_list = get_atc()
        if not atc_list:
            self.info_label.configure(text=self.t("no_atc"))
            return

        closest = find_nearest_atc(pos, atc_list)
        if not closest:
            self.info_label.configure(text=self.t("no_position"))
            return

        self.info_label.configure(
            text=f"{closest['callsign']}\n{closest.get('frequency', 'N/A')} MHz\n{closest['distance_nm']} NM"
        )

        if should_alert(closest, self.alert_distance):
            if self.last_alerted != closest["callsign"]:
                self.last_alerted = closest["callsign"]

                msg = f"{self.t('alert_msg')}: {closest['callsign']} — {closest['distance_nm']} NM"

                notification.notify( # type: ignore[call]
                    title=self.t("alert_title"),
                    message=msg,
                    timeout=6
                )

                self._send_ntfy(msg)
        else:
            self.last_alerted = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
