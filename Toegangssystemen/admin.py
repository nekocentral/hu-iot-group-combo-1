import parkeerplaatsen as p
import toegangruimtes as t
import qr as q

parkeer = p.Parkeren()
toegang = t.Toegang()
qr_code = q.qr()

qr_code.new_qr_user('Ralph', 'van Leeuwen', 'info@anvion.nl')