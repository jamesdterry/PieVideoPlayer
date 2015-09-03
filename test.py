import shelve

# Open database, creating it if necessary.
db = shelve.open('datastore', 'c')

# Record some values
db['www.python.org'] = 'Python Website'
db['www.cnn.com'] = 'Cable News Network'
db['videos'] = ['a', 'b', 'c']

# Loop through contents.  Other dictionary methods
# such as .keys(), .values() also work.
for k, v in db.iteritems():
    print k, '\t', v

# Close when done.
db.close()