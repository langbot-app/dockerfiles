"""Run inside a fresh sandbox without installing packages or selecting a font."""

import io
import os
from pathlib import Path
import unittest
import warnings


class SandboxChartTests(unittest.TestCase):
    def test_pandas_is_preinstalled(self):
        import pandas as pd

        frame = pd.read_csv(io.StringIO("月份,收入\n一月,-2\n二月,3\n"))
        self.assertEqual(frame["收入"].sum(), 1)

    def test_default_matplotlib_renders_chinese(self):
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib import font_manager, ft2font

        self.assertEqual(matplotlib.get_backend().lower(), "agg")
        font_path = font_manager.findfont(font_manager.FontProperties())
        glyphs = ft2font.FT2Font(font_path).get_charmap()
        text = "中文图表月份收入繁體測試−"
        self.assertTrue(all(ord(char) in glyphs for char in text), font_path)
        with warnings.catch_warnings():
            warnings.filterwarnings("error", message=r"Glyph .* missing from font")
            fig, ax = plt.subplots()
            ax.plot([-1, 0, 1], [-2, 0, 3], label="收入")
            ax.set(title="中文图表 / 繁體測試", xlabel="月份", ylabel="收入")
            ax.legend()
            output = io.BytesIO()
            fig.savefig(output, format="png")
            plt.close(fig)
        self.assertTrue(output.getvalue().startswith(b"\x89PNG\r\n\x1a\n"))
        if target := os.environ.get("CHART_TEST_OUTPUT"):
            Path(target).write_bytes(output.getvalue())
        print(f"Default font: {font_path}; PNG bytes: {len(output.getvalue())}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
