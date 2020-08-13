#!/bin/bash

#reparar permisos
sudo chown -R root:root deepines-store_1.2/
sudo chown -R root:root deepines-store_1.2/usr/

#empaquetar
dpkg-deb --build deepines-store_1.2/