from hypothesis import settings

settings.register_profile("full", max_examples=1000)
settings.register_profile("dev", max_examples=10)
settings.register_profile("debug", max_examples=2)
