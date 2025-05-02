import time, winsound

def hh_mm():
    tm = input('Установить время (оставьте поле пустым для отмены): ')
    if tm == '':
        return None
    elif len(tm.split(':')) == 2:
        hh, mm = map(int, tm.split(':'))
        if 0 <= hh < 24 and 0 <= mm < 60:
            return hh, mm
    else:
        print('формат должен быть ЧЧ:ММ')
    return hh_mm()
def signal_type():
    st = input('Звуковое уведомление? y/n или название файла из каталога: ')
    if st == 'n' or st == '':
        st = None
    elif st == 'y':
        st = 'default'
    return st
def alarm(signal):
    print(f'{time.strftime('%H:%M')} Время вставать!')
    if signal:
        try:
            winsound.PlaySound(signal, winsound.SND_NODEFAULT)
        except RuntimeError:
            winsound.Beep(1500, 3000)

all_tms = {}
while True:
    cl = hh_mm()
    if not cl:
        break
    elif all_tms.get(cl[0]):
        all_tms[cl[0]][cl[1]] = signal_type()
    else:
        all_tms[cl[0]] = {cl[1] : signal_type()}
while True:
    cur_hr = time.localtime().tm_hour
    cur_mn = time.localtime().tm_min
    cur_sc = time.localtime().tm_sec
    if not all_tms:
        print('Будильник не установлен!')
        break
    elif cur_hr in all_tms:
        if cur_mn in all_tms[cur_hr]:
            alarm(all_tms[cur_hr][cur_mn])
        time.sleep(60 - cur_sc)
    else:
        time.sleep((60 - cur_mn) * 60 - cur_sc)