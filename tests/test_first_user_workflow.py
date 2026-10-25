"""First-use authoring checkpoints that need no cloud accounts."""
from pathlib import Path
import tempfile
import json
import unittest
from greedyq.build import build

ROOT=Path(__file__).resolve().parents[1]


class FirstUserWorkflowTests(unittest.TestCase):
    def test_researcher_written_start_has_only_opening_and_ending_then_accepts_questions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            qmd='''---
title: "Researcher-written draft"
greedyq:
  spec_version: "0.2"
  version: "RELEASE"
  organization: "Example Team"
survey-settings:
  start-page: welcome
---

--- welcome

# Welcome

Draft only. Participant information is not finalized.

--- complete

# Thank you
'''
            qmd=qmd.replace("RELEASE",json.loads((ROOT/"release.json").read_text())["release"])
            (root/'survey.qmd').write_text(qmd)
            (root/'greedyq.yml').write_text('''spec_version: "0.2"
study:
  id: researcher_written_draft
  title: Researcher-written draft
  version: draft
respondents:
  source: direct_link
  mode: test
outcomes:
  complete:
    page: complete
    lifecycle_state: completed
''')
            report,model=build(root)
            self.assertEqual('passed',report['status'],report)
            self.assertEqual(['welcome','complete'],[p['id'] for p in model['pages']])
            self.assertEqual([], [q for p in model['pages'] for q in p['questions']])
            supplied='''--- feedback

# Your feedback

```{r}
sd_question(id = "first", type = "text", label = "What worked?")
```

```{r}
sd_question(id = "second", type = "textarea", label = "What should improve?")
```

'''
            (root/'survey.qmd').write_text(qmd.replace('--- complete',supplied+'--- complete'))
            report,model=build(root)
            self.assertEqual('passed',report['status'],report)
            self.assertEqual(['first','second'],[q['id'] for p in model['pages'] for q in p['questions']])
            self.assertTrue((root/'preview.html').is_file())

    def test_reference_consent_information_is_in_the_rendered_page(self):
        for name in ('complete-study','simple-satisfaction-study'):
            with self.subTest(name=name):
                report,model=build(ROOT/'examples'/name,write=False)
                self.assertEqual('passed',report['status'],report)
                body=next(p['body'] for p in model['pages'] if p['id']=='consent')
                self.assertIn('1.1.0',body)
                self.assertIn('Voluntary participation and withdrawal',body)
                self.assertIn('researcher@example.',body)
                self.assertNotIn('(./consent.md)',body)
