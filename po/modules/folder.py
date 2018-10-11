import pathlib
import os




def build_job(root, client, project, job):
    # TODO: figure out error proof way of using project code
    # TODO: Imple folder struct in code
    base = pathlib.Path(root, client, project, job)

    # Creative Dir
    pathlib.Path(base).joinpath('creative', 'branding & identity', 'draft design').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('creative', 'branding & identity', 'final design').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('creative', 'branding & identity', 'ref imagery').mkdir(parents=True, exist_ok=False)

    pathlib.Path(base).joinpath('creative', 'presentations').mkdir(parents=True, exist_ok=False)

    pathlib.Path(base).joinpath('creative', 'print & brochures', 'draft design').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('creative', 'print & brochures', 'final design').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('creative', 'print & brochures', 'ref imagery').mkdir(parents=True, exist_ok=False)

    pathlib.Path(base).joinpath('creative', 'web & interactive', 'draft design').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('creative', 'web & interactive', 'final design').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('creative', 'web & interactive', 'ref imagery').mkdir(parents=True, exist_ok=False)

    # deliverables
    pathlib.Path(base).joinpath('deliverables').mkdir(parents=True, exist_ok=False)

    # still and film
    pathlib.Path(base).joinpath('still & film', 'assets').mkdir(parents=True, exist_ok=False)

    pathlib.Path(base).joinpath('still & film', 'max files', 'animation', 'context').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'max files', 'animation', 'master').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'max files', 'animation', 'scene').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'max files', 'still imagery', 'context').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'max files', 'still imagery', 'master').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'max files', 'still imagery', 'scene').mkdir(parents=True, exist_ok=False)

    pathlib.Path(base).joinpath('still & film', 'renders', 'animation', 'composites').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'animation', 'final films').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'animation', 'sequences + footage').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'animation', 'still imagery').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'animation', 'still imagery', 'jpg').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'animation', 'still imagery', 'psd').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'animation', 'still imagery', 'tga').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'draft renders', 'jpg').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'draft renders', 'psd').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'draft renders', 'tga').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'exterior images', 'jpg').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'exterior images', 'psd').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'exterior images', 'tga').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'interior images', 'jpg').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'interior images', 'psd').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'interior images', 'tga').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'wireframe', 'jpg').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'wireframe', 'psd').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('still & film', 'renders', 'stills', 'wireframe', 'tga').mkdir(parents=True, exist_ok=False)

    # support
    pathlib.Path(base).joinpath('support', 'sent').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('support', 'ad').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('support', 'comments', 'MM.DD.YY-desc').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('support', 'issued information', 'MM.DD.YY-desc').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('support', 'photography', 'MM.DD.YY-desc').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('support', 'project schedule').mkdir(parents=True, exist_ok=False)
    pathlib.Path(base).joinpath('support', 'reference imagery').mkdir(parents=True, exist_ok=False)

    # pathlib.Path(two).mkdir(parents=True, exist_ok=False)

    return True
    
    