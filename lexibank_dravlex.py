from pathlib import Path

import attr
from pycldf import Wordlist
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import Cognate, Language, FormSpec


@attr.s
class CustomCognate(Cognate):
    Comment = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    concept_count = attr.ib(default=None)
    word_count = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "dravlex"
    language_class = CustomLanguage
    cognate_class = CustomCognate

    form_spec = FormSpec(
        brackets={"[": "]", "{": "}", "(": ")"},
        separators=";/,~",
        missing_data=('-', ),
        strip_inside_brackets=True,
    )

    def cmd_makecldf(self, args):
        dsdir = self.dir / 'raw' / 'Verkerk-DravLex-622ac6e'

        # load concepts
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split('-')[-1]+ '_' + slug(c.english), lookup_factory="Name"
        )

        # load sources from original CLDF, and then the fieldwork source
        args.writer.add_sources(*self.raw_dir.read_bib(dsdir / 'sources.bib'))
        args.writer.add_sources()
        
        # load languages
        args.writer.add_languages()

        # load cognates
        cogs = {
            r['Form_ID']: r for r in self.raw_dir.read_csv(dsdir / 'cognates.csv', dicts=True)
        }
        
        # load data
        for row in self.raw_dir.read_csv(dsdir / 'forms.csv', dicts=True):
            src = row['Source'].split(";") if row['Source'] else ['KolipakamFW']
            cog = cogs.get(row['ID'])
            for lex in args.writer.add_forms_from_value(
                Local_ID=row['ID'],
                Language_ID=row['Language_ID'],
                Parameter_ID=concepts[row['Parameter_ID']],
                Value=row['Form'],
                Source=src,
                Comment=row['status'],
                Loan=True if row['status'] else False
            ):
                args.writer.add_cognate(
                    lexeme=lex,
                    ID=cog['ID'],
                    Source=cog['Source'],
                    Cognateset_ID=cog['Cognateset_ID'],
                    Comment=", ".join([cog['Comment'], cog['source_comment']])
                )
