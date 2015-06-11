A birds eye overview
====================

A MultiPageForm has one MultiForm per page. Each MultiForm has a name. Both
MultiPageForms and MultiForms behave like **django.form.Form**\s otherwise.

A MultiForm combines two or more forms into one, so that they can be treated as
one form. It consists of:

* an automatically created ControlForm with a hidden ``field seen``, which is
  used by MultiPageForm to know whether the page has been visited or not.
* one or more regular **django.form.Form**\s.

Each Form inside the MultiForm has its position as part of its name: the
ControlForm is always form 0.

A MultiForm can be in one of three states: unseen, invalid and valid. A
MultiPageForm has only two states: invalid and valid, depending on whether its
MultiForms are all invalid or valid.

.. image:: multipageform-overview.svg

The views working on the MultiForms and MultiPageForms serializes the
**django.form.Form.data** field as JSON. When you save the page you're
currently on, the views assure that only the data belonging to that MultiForm
is changed. They also set ``ControlForm.seen`` to True.
