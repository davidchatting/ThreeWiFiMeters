#needs to run as root to show all networks - not just the one you are connected to
import wifi

def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False

def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False

def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')

    for cell in cells:
        wifilist.append(cell)

    return wifilist

def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme

def connect(ssid, password=None):
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()   # ifup and ifdown do not work on raspbian stretch

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False

                return cell
    
    return False

def scanForCells():
	#uses iwlist
    cells = list(wifi.Cell.all('wlan0'))

    for cell in cells:
        cell.summary = '{} ({})  Channel {}'.format(cell.ssid, cell.frequency, cell.channel)

        # if cell.encrypted:
        #     enc_yes_no = '*'
        # else:
        #     enc_yes_no = '()'

        #cell.summary = cell.summary + ' / Encryption {}'.format(enc_yes_no)

    return cells

cells = scanForCells()
for cell in cells:
    print(cell.summary)

connect('BTHub4-W3MZ 2.4GHz', '2426adca59')
