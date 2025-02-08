import sys

import os
import subprocess
import unittest
from test.support.script_helper import kill_python


def spawn_repl(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT):
    # To run the REPL without using a terminal, spawn python with the command
    # line option '-i' and the process name set to '<stdin>'.
    # The directory of argv[0] must match the directory of the Python
    # executable for the Popen() call to python to succeed as the directory
    # path may be used by Py_GetPath() to build the default module search
    # path.
    stdin_fname = os.path.join(os.path.dirname(sys.executable), "<stdin>")
    cmd_line = [stdin_fname, "-c", f"from asyncio import console;{cmd}"]

    # Set TERM=vt100, for the rationale see the comments in spawn_python() of
    # test.support.script_helper.
    env = dict(os.environ)
    env['TERM'] = 'vt100'
    return subprocess.Popen(cmd_line,
                            executable=sys.executable,
                            text=True,
                            stdin=subprocess.PIPE,
                            stdout=stdout, stderr=stderr,
                            )


class TestInteract(unittest.TestCase):
    def test_set_banner(self):
        p = spawn_repl("console.interact(banner='hello from my console')")
        output = kill_python(p)
        self.assertEqual(p.returncode, 0)
        expected = "hello from my console"
        self.assertStartsWith(output, expected)

    def test_set_exitmsg(self):
        p = spawn_repl("console.interact(exitmsg='quitting console')")
        output = kill_python(p)
        self.assertEqual(p.returncode, 0)
        expected = "quitting console"
        self.assertEndsWith(output, expected)

    def test_set_local(self):
        p = spawn_repl("console.interact(local={'my_var': 'content of my_var'})")
        p.stdin.write('my_var')
        output = kill_python(p)
        self.assertEqual(p.returncode, 0)
        self.assertIn('content of my_var', output)


if __name__ == "__main__":
    unittest.main()
