# py_cmd_exec 

Execute external command

## Usage

```
>>> from py_cmd_exec import CMDExec
>>> exec = CMDExec(['date', '+%F'])
>>> exec.execute()
INFO:py_cmd_exec:executing ['date', '+%F']
DEBUG:py_cmd_exec:attempting blocking execution of ['date', '+%F']
(0, ['date', '+%F'], '2017-06-27\n', '')
>>>
```

## Security

See [Security Considerations](https://docs.python.org/3/library/subprocess.html#security-considerations) of `subprocess` module.

## Contributing

You are more then welcome to fork it and contribute by creating pull requests.
In case of any other need, please let me know.

Please make sure your code is compliant with [PEP8 standard](https://www.python.org/dev/peps/pep-0008/), with some tweaks allowed:

* E402 - in tests, module-level imports not being placed at the top of the source file are fine.
* E501 - maximum line length is set to 92 characters (more practical and still tidy / readable)
* E265 - it is OK to comment code without adding space after `#`

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt); see [LICENSE.txt](LICENSE.txt)  
Copyright © 2017, 2018 Filip M. Nowak
