g_scan_keys = []
for iy in range (-1,2):
    for ix in range (-1,2):
        for iz in range (-1,2):
            g_scan_keys.append([g_loc[0] + ix, g_loc[1] + iy, g_loc[1] + iz])
print (count)
