

import fill_database

# Eerst ruimtes genereren
fill_database.new_ruimte(1, 'Fietsenstalling')
fill_database.new_ruimte(2, 'Server ruimte')
fill_database.new_ruimte(3, 'Medischeinen hok')
fill_database.new_ruimte(4, 'Kroeg')
fill_database.new_ruimte(5, 'Slaapkamer')

# Deze doen per persoon
persoons_id = fill_database.new_person('Ralph', 'van Leeuwen', 1, 1)
fill_database.new_tag(6666, 1, 0, persoons_id)
fill_database.new_toegang(persoons_id, 1, 1)
fill_database.new_toegang(persoons_id, 2, 0)
fill_database.new_toegang(persoons_id, 3, 1)
fill_database.new_toegang(persoons_id, 4, 0)
fill_database.new_toegang(persoons_id, 5, 1)

persoons_id = fill_database.new_person('Sven', 'Visser', 1, 0)
fill_database.new_tag(1111, 0, 1, persoons_id)
fill_database.new_toegang(persoons_id, 1, 0)
fill_database.new_toegang(persoons_id, 2, 1)
fill_database.new_toegang(persoons_id, 3, 0)
fill_database.new_toegang(persoons_id, 4, 1)
fill_database.new_toegang(persoons_id, 5, 0)

persoons_id = fill_database.new_person('Cornelis', 'Stuurman', 0, 1)
fill_database.new_tag(2222, 1, 1, persoons_id)
fill_database.new_toegang(persoons_id, 1, 1)
fill_database.new_toegang(persoons_id, 2, 1)
fill_database.new_toegang(persoons_id, 3, 1)
fill_database.new_toegang(persoons_id, 4, 1)
fill_database.new_toegang(persoons_id, 5, 1)

persoons_id = fill_database.new_person('Ruben', 'van der Weide', 0, 0)
fill_database.new_tag(3333, 0, 0, persoons_id)
fill_database.new_toegang(persoons_id, 1, 0)
fill_database.new_toegang(persoons_id, 2, 0)
fill_database.new_toegang(persoons_id, 3, 0)
fill_database.new_toegang(persoons_id, 4, 0)
fill_database.new_toegang(persoons_id, 5, 0)