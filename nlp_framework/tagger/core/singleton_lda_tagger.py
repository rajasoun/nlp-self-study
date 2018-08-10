from tagger.core import LDATagger


class SingletonLDATagger:
    lda_tagger = None

    @classmethod
    def lda_tagger(cls, *ars, **kwargs):
        if not cls.lda_tagger:
            cls.lda_tagger = LDATagger(*ars, **kwargs)
        return cls.lda_tagger
