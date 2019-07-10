import attr
from clldutils.path import Path
from pycldf.dataset import Wordlist
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Cognate


@attr.s
class DravidianCognate(Cognate):
    Comment = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "dravlex"
    cognate_class = DravidianCognate

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):

        dsdir = self.dir / 'raw' / 'Verkerk-DravLex-622ac6e'

        dataset = Wordlist.from_metadata(dsdir / 'Wordlist-metadata.json')

        with self.cldf as ds:
            ds.add_concepts(id_factory=lambda c: c.english)
            # add sources from original CLDF, and then the fieldwork source
            ds.add_sources(*self.raw.read_bib(dsdir / 'sources.bib'))
            ds.add_sources(*self.raw.read_bib())

            for row in self.raw.read_csv(dsdir / 'languages.csv', dicts=True):
                # remove un-needed fields
                del(row['concept_count'])
                del(row['word_count'])
                ds.add_language(**row)


            # load cognates
            cogs = {}
            for row in self.raw.read_csv(dsdir / 'cognates.csv', dicts=True):
                cogs[row['Form_ID']] = row

            for row in self.raw.read_csv(dsdir / 'forms.csv', dicts=True):
                src = row['Source'].split(";") if row['Source'] else ['KolipakamFW']
                cog = cogs.get(row['ID'])
                for lex in ds.add_lexemes(
                    Local_ID=row['ID'],
                    Language_ID=row['Language_ID'],
                    Parameter_ID=row['Parameter_ID'],
                    Value=row['Form'],
                    Source=src,
                    Comment=row['status'],
                    Cognacy=cog,
                    Loan=True if row['status'] else False
                ):
                    ds.add_cognate(
                        lexeme=lex,
                        ID=cog['ID'],
                        Source=cog['Source'],
                        Cognateset_ID=cog['Cognateset_ID'],
                        Comment=", ".join([cog['Comment'], cog['source_comment']])
                    )


