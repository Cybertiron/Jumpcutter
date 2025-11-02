"""Entry point for running the Jumpcutter GUI application."""

from jumpcutter import JumpCutterApp


def main() -> None:
    app = JumpCutterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
