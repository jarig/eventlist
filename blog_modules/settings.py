from blog_modules import models as modules

MODULE_SECRET = "module_secret_secret"


INSTALLED_MODULES = {
    modules.ImageSlider.hash: modules.ImageSlider(),
    modules.Dummy.hash: modules.Dummy()
}

MODULES = {#position: [module list]
    u'default': {
        1: [modules.Dummy],
        2: [modules.ImageSlider]
    }
}

#