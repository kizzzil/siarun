## SIARUN - сканер уязвимостей.
структура программы разделена на 3 модуля:
* scanning - модуль предназначенный для определения цели и проведения сканирования сети/ресурса а далее выборка версий программного обеспечения. В данный момент состоит из 3х подмодулей.
  * перечисление поддоменов
  * краулинг
  * сканирование портов
* identify vulns - сапоставление найденных версий ПО с различными БДУ. В данный момент это NIST NVD, есть возмодность дописания модулей для NNVD и БДУ ФСТЭК
* getting access - времено не запушен 

### quick start

```
git clone https://github.com/kizzzil/siarun
cd siarun
main.py targetsute.com
```
<img src="https://telegra.ph/file/277d2bbf8815a0b67b87f.jpg">
