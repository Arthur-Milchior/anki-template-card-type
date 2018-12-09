Each file correspond to one kind of tag.

Each file must:
* have a method compile_(tag, soup, **kwargs). It adds the content to the tag, and return the string of new contents. It may assume there is no content currently. kwargs may be arguments used for other modules.
* Have a method clean(tag), cleaning params potentially added by this module. The contents is cleaned by the caller.
* call templates.addKindOfTemplate(templateParameter, sys.modules[__name__]), stating that if «tempplate = templateParameter» occurs in a Span tag, the current module must be used on it.

Current templates are:
* objects: call an element from the config file
* front side: the equivalent of {{FrontSide}}. But adapted to the fact that it is a question side.

Current keywords arguments passed are:
* isQuestion: whether the template appears on question side
* model: the model from which it is called
* objects: the list of objects defined in the config.
* FrontSide: the front side related to this backside