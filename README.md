# Vidi URLs Plugin

Quick, relevant links to Vidispine from within Portal.


## Install
* Set the `Domain name` in the System settings
* chmod setup.sh
* Run setup.sh
```
$ chmod +x setup.sh
$ sudo ./setup.sh
```

## ToDo
* Write tests
* Fix install script to put the HTML into the base template (and metadatamanagement template)
* Add ability to close / hit urls (if they obscure something)

## Bugs
* Specific storage URL does not match
* /vs/index/ and /search/last/10/ do not hit the plugin
* Stop part matches e.g. /user/ is matched with /user/admin/


#### Example Screen shot
![Example screen shot](http://i.imgur.com/ylD4i02.png?1?raw=true "Example screen shot")
