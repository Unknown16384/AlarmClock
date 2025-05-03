import time, winsound

def hh_mm():
    tm = input('Установить время (оставьте поле пустым для отмены): ')
    if tm == '':
        return None
    else:
        try:
            if len(tm.split(':')) == 2:
                hh, mm = map(int, tm.split(':'))
                if 0 <= hh < 24 and 0 <= mm < 60:
                    return hh, mm
            raise ValueError
        except ValueError:
            print('формат должен быть ЧЧ:ММ')
            return hh_mm()
def signal_type():
    st = input('Звуковое уведомление (Y/N или название файла из каталога): ')
    if st.lower() == 'n' or st == '':
        st = None
    elif st.lower() == 'y':
        st = 'default'
    return st
def repeat():
    rp = input('Повторять (Y/N или дни недели через пробел): ')
    if rp.lower() == 'n' or rp == '':
        return False
    elif rp.lower() == 'y':
        return {0, 1, 2, 3, 4, 5, 6}
    else:
        wkl = set()
        for d in rp.split(' '):
            if d.lower() in ['0', 'понедельник', 'пн', 'monday', 'mon', 'mn']:
                wkl.add(0)
            elif d.lower() in ['1', 'вторник', 'вт', 'tuesday', 'tue', 'tu']:
                wkl.add(1)
            elif d.lower() in ['2', 'среда', 'ср', 'wednesday', 'wed', 'wd']:
                wkl.add(2)
            elif d.lower() in ['3', 'четверг', 'чтв', 'чт', 'thursday', 'thu', 'th']:
                wkl.add(3)
            elif d.lower() in ['4', 'пятница', 'пт', 'friday', 'fri', 'fr']:
                wkl.add(4)
            elif d.lower() in ['5', 'суббота', 'сбт', 'сб', 'saturday', 'sat', 'sa']:
                wkl.add(5)
            elif d.lower() in ['6', 'воскресенье', 'вс', 'sunday', 'sun', 'sn']:
                wkl.add(6)
            else:
                print('Неправильный формат ввода')
                break
        else:
            return wkl
        return repeat()
def alarm(signal):
    print(f'{time.strftime('%H:%M')} Время вставать!')
    if signal:
        try:
            winsound.PlaySound(signal, winsound.SND_NODEFAULT)
        except RuntimeError:
            winsound.Beep(1500, 3000)
def del_check():
    if input('Отключить этот будильник (Y/любое другое значение для "N"): ').lower() == 'y':
        return True
    else:
        return False
all_tms = {}
while True:
    cl = hh_mm()
    if not cl:
        break
    elif all_tms.get(cl[0]):
        all_tms[cl[0]][cl[1]] = (signal_type(), repeat())
    else:
        all_tms[cl[0]] = {cl[1] : (signal_type(), repeat())}
while True:
    cur_wd = time.localtime().tm_wday
    cur_hr = time.localtime().tm_hour
    cur_mn = time.localtime().tm_min
    cur_sc = time.localtime().tm_sec
    if not all_tms:
        break
    elif cur_hr in all_tms:
        if not all_tms[cur_hr]:
            del all_tms[cur_hr]
            continue
        elif cur_mn in all_tms[cur_hr]:
            if not all_tms[cur_hr][cur_mn][1]:
                alarm(all_tms[cur_hr][cur_mn][0])
                del all_tms[cur_hr][cur_mn]
                continue
            elif cur_wd in all_tms[cur_hr][cur_mn][1]:
                alarm(all_tms[cur_hr][cur_mn][0])
                if del_check():
                    del all_tms[cur_hr][cur_mn]
                    continue
        time.sleep(60 - cur_sc)
    else:
        time.sleep((60 - cur_mn) * 60 - cur_sc)