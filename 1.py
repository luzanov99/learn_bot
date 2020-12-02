import ephem 
active_planet=ephem.Uranus('2020/10/10')
constellation = ephem.constellation(active_planet)
print(constellation)