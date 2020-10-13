

import fill_database

# Eerst ruimtes genereren
fill_database.new_ruimte(1, 'Fietsenstalling')
fill_database.new_ruimte(2, 'Server ruimte')
fill_database.new_ruimte(3, 'Medischeinen hok')
fill_database.new_ruimte(4, 'Kroeg')
fill_database.new_ruimte(5, 'Slaapkamer')

# Deze doen per persoon
persoons_id = new_person('Ralph', 'van Leeuwen', 1, 1)
fill_database.new_tag(6666, 1, 0, persoons_id)
fill_database.new_toegang(persoons_id, 1, 1)
fill_database.new_toegang(persoons_id, 2, 0)
fill_database.new_toegang(persoons_id, 3, 1)
fill_database.new_toegang(persoons_id, 4, 0)
fill_database.new_toegang(persoons_id, 5, 1)