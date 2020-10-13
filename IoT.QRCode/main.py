import parkeerplaatsen as p

sven = p.Parkeren()
print(sven.tel_parkeerplaatsen())
print(sven.tel_voorangparkeerplaatsen())
persoon = (sven.get_persoonid(5555))
print(sven.check_parkeer(persoon))
print(sven.check_voorang(persoon))

print(sven.parkeer(5555, 1))