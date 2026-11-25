import importlib.util, unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/"tools"/"validate_project.py"
spec=importlib.util.spec_from_file_location("validate_project",SCRIPT)
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class ProjectValidatorTests(unittest.TestCase):
    def test_stable_ids(self):
        self.assertTrue(module.ID_PATTERNS["C"].fullmatch("C001"))
        self.assertTrue(module.ID_PATTERNS["E"].fullmatch("E123"))
        self.assertFalse(module.ID_PATTERNS["D"].fullmatch("D12"))
    def test_project_checks_do_not_include_skill_files(self):
        self.assertIn("episode-outline",module.REQUIRED)
        self.assertIn("review-report",module.REQUIRED)
        self.assertNotIn("SKILL.md",module.REQUIRED)

if __name__=="__main__": unittest.main()
