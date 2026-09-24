import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prepare_release import TARGETS, prepare


class ReleaseAssetsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'input'
        self.output = self.root / 'output'
        self.files = []
        for target in TARGETS:
            folder = self.source / f'LEGv8-0.71-{target}-unsigned'
            folder.mkdir(parents=True)
            suffix = 'tar.gz' if target == 'linux-x64' else 'zip'
            file = folder / f'LEGv8-0.71-{target}.{suffix}'
            file.write_bytes(target.encode())
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            (folder / 'SHA256SUMS.txt').write_text(f'{digest}  {file.name}\n')
            self.files.append(file)

    def test_complete_build_combines_checksums_without_collisions(self):
        prepare(self.source, self.output)
        self.assertEqual(len(list(self.output.iterdir())), 5)
        self.assertEqual(len((self.output / 'SHA256SUMS.txt').read_text().splitlines()), 4)
        for file in self.files:
            self.assertEqual(file.read_bytes(), (self.output / file.name).read_bytes())

    def test_missing_platform_cannot_prepare_partial_release(self):
        self.files[-1].unlink()
        with self.assertRaisesRegex(ValueError, 'Missing package'):
            prepare(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_corrupt_package_is_rejected(self):
        self.files[0].write_bytes(b'corrupted')
        with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
            prepare(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_manifest_cannot_substitute_another_file(self):
        checksum = self.files[0].parent / 'SHA256SUMS.txt'
        checksum.write_text(checksum.read_text().replace(self.files[0].name, '../other.zip'))
        with self.assertRaisesRegex(ValueError, 'Unexpected checksum'):
            prepare(self.source, self.output)


if __name__ == '__main__':
    unittest.main()
