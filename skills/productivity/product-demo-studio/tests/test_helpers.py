import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]

def run(script, *args):
    return subprocess.run([sys.executable, str(SKILL/'scripts'/script), *map(str,args)], capture_output=True, text=True, timeout=120)

class Helpers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root/'Demo project'
    def tearDown(self):
        self.temp.cleanup()
    def init(self):
        result = run('init_project.py', '--output', self.project, '--name', 'Acme Demo')
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((self.project/'project.json').read_text())
    def test_init_is_portable_and_does_not_overwrite(self):
        data = self.init()
        self.assertFalse(data['approved'])
        self.assertEqual(data['product']['name'], 'Acme Demo')
        self.assertTrue((self.project/'src/Root.tsx').exists())
        self.assertTrue((self.project/'support/check_project.py').exists())
        (self.project/'keep.txt').write_text('user owned')
        self.assertNotEqual(run('init_project.py','--output',self.project,'--name','Other').returncode,0)
        self.assertEqual((self.project/'keep.txt').read_text(),'user owned')
    def test_unapproved_or_incomplete_brief_cannot_render(self):
        self.init()
        result = run('check_project.py',self.project)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('approved',result.stdout+result.stderr)
    def test_dependency_plan_has_seven_pins_and_no_download(self):
        result = run('fetch_workflows.py','--output',self.root/'tools','--ids','all')
        self.assertEqual(result.returncode,0,result.stderr)
        rows = json.loads(result.stdout)['workflows']
        self.assertEqual([r['id'] for r in rows], [f'C{i:02}' for i in range(1,8)])
        self.assertTrue(all(len(r['commit'])==40 for r in rows))
        self.assertFalse((self.root/'tools').exists())
    def test_missing_delivery_does_not_pass_verification(self):
        self.init()
        result = run('verify_media.py',self.project)
        self.assertNotEqual(result.returncode,0)
    def test_gallery_rejects_path_escape(self):
        self.init()
        (self.project/'delivery.json').write_text(json.dumps({'product':'Acme','locales':[{'id':'en','label':'English'}],'rows':[{'id':'C03','locale':'en','format':'portrait','name':'Demo','src':'../private.mp4','poster':'../private.jpg'}]}))
        result = run('build_review.py',self.project,'--output',self.root/'review')
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.root/'review').exists())

if __name__ == '__main__':
    unittest.main()
