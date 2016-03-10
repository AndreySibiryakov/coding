#SC02E::

FormatTime, currTime, , dd.MM.yyyy

Clipboard =
Send ^{SC02E}
ClipWait,,1
workTime := Clipboard

StringReplace, workTime, workTime, :, , All
StringSplit, workTimeList, workTime, %A_Tab%, dev, All

startTime = 20000101%workTimeList2%
endTime = 20000101%workTimeList3%

EnvSub, endTime, %startTime%, minutes	
subTime =
subTime := endTime - 540

bodyMessage =
if subTime >= 20
      bodyMessage = %currTime%`nСегодня я отработал %subTime% мин.
if subTime <= -20
{
      StringTrimLeft, subTime, subTime, 1
      bodyMessage = %currTime%`nСегодня я ушел раньше на %subTime% мин.`n Отработаю в скором времени.
}

tox     =nikita.samusenko@frogwares.com, serge@frogwares.com   ; adress 
subject =отчет по рабочему времени 
body    =FollowedLine1`%0AFollowedLine2
dates   =%a_now%
      TO=to='%TOX%'
      PR=c:\Program Files (x86)\Mozilla Thunderbird\thunderbird.exe
      SB=subject=%subject%
      AT=attachment='%FILEX%'
      BD=body= %bodyMessage%
      ;~ body=Hallo Garry`%0A`%0AHow are you ?`%0A`%0A%body%`%0A`%0AGreetings`%2C`%0A garry`%0A`%0A`%0A%dates%
      ALL=%TO%,%SB%,%AT%,%BD%
      run,%PR% -compose "%ALL%"
reload