import pytest
import aisquared


def test_steps_init():
    aisquared.config.preprocessing.text.Tokenize()
    aisquared.config.preprocessing.text.RemoveCharacters()
    aisquared.config.preprocessing.text.ConvertToCase()
    aisquared.config.preprocessing.text.ConvertToVocabulary(
        {
            'this': 3,
            'is': 4,
            'a': 5,
            'test': 6
        }
    )
    aisquared.config.preprocessing.text.PadSequences()
    aisquared.config.preprocessing.text.Trim()

    aisquared.config.preprocessing.image.AddValue(10)
    aisquared.config.preprocessing.image.SubtractValue(10)
    aisquared.config.preprocessing.image.MultiplyValue(10)
    aisquared.config.preprocessing.image.DivideValue(10)
    aisquared.config.preprocessing.image.ConvertToColor('RGB')
    aisquared.config.preprocessing.image.Resize([10, 10])

    aisquared.config.preprocessing.tabular.ZScore([0, 0, 0], [1, 1, 1])
    aisquared.config.preprocessing.tabular.MinMax([0, 0, 0], [1, 1, 1])
    aisquared.config.preprocessing.tabular.OneHot(2, ['cat', 'dog', 'lizard'])
    aisquared.config.preprocessing.tabular.DropColumn(4)


def test_processers_init():
    tabular = aisquared.config.preprocessing.tabular.TabularPreprocesser()
    image = aisquared.config.preprocessing.image.ImagePreprocesser()
    text = aisquared.config.preprocessing.text.TextPreprocesser()

    tabular.add_step(
        aisquared.config.preprocessing.tabular.ZScore([0], [0])
    )
    image.add_step(
        aisquared.config.preprocessing.image.SubtractValue(10)
    )
    text.add_step(
        aisquared.config.preprocessing.text.RemoveCharacters()
    )

    with pytest.raises(TypeError):
        tabular.add_step(
            aisquared.config.preprocessing.text.RemoveCharacters()
        )
        image.add_step(
            aisquared.config.preprocessing.tabular.ZScore([0], [0])
        )
        text.add_step(
            aisquared.config.preprocessing.image.SubtractValue(10)
        )
