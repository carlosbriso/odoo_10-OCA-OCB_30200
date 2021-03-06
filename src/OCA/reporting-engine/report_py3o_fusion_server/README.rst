.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==========================================
Py3o Report Engine - Fusion server support
==========================================

This module was written to let a py3o fusion server handle format conversion instead of local libreoffice. If you install this module above the *report_py3o* module, you will have to deploy additionnal software components and run 3 daemons (libreoffice, py3o.fusion and py3o.renderserver). This additionnal complexiy comes with several advantages:

* much better performances (Libreoffice runs permanently in the background, no need to spawn a new Libreoffice instance upon every document conversion).
* ability to configure PDF export options in Odoo. This brings many new possibilities such as the ability to generate:

  * PDF forms
  * PDF/A documents (required by some electronic invoicing standards such as `Factur-X <http://fnfe-mpe.org/factur-x/>`_)
  * watermarked PDF documents
  * password-protected PDF documents

Installation
============

Install several additional components and Python libs:

* `Py3o Fusion server <https://bitbucket.org/faide/py3o.fusion>`_,
* `Py3o render server <https://bitbucket.org/faide/py3o.renderserver>`_,
* a Java Runtime Environment (JRE), which can be OpenJDK,
* Libreoffice started in the background in headless mode,
* the Java driver for Libreoffice (Juno).

It is also possible to use the Python driver for Libreoffice (PyUNO), but it is recommended to use the Java driver because it is more stable.

The installation procedure below uses the Java driver. It has been successfully tested on Ubuntu 16.04 LTS ; if you use another OS, you may have to change a few details.

Installation of Libreoffice, JRE and required Java libs on Debian/Ubuntu:

.. code::

  sudo apt-get install default-jre ure libgoogle-gson-java libreoffice-java-common libreoffice-writer

You may have to install additionnal fonts. For example, to have the special unicode symbols for phone/fax/email in the PDF reports generated by Py3o, you should install the following package:

.. code::

  sudo apt-get install fonts-symbola

Installation of py3o.fusion:

.. code::

  pip install py3o.fusion
  pip install service-identity

Installation of py3o.renderserver:

.. code::

  pip install py3o.renderserver

At the end, with the dependencies, you should have the following py3o python libs:

.. code::

  % pip freeze | grep py3o
  py3o.formats==0.3
  py3o.fusion==0.8.8
  py3o.renderclient==0.2
  py3o.renderers.juno==0.8
  py3o.renderserver==0.5.1
  py3o.template==0.9.12
  py3o.types==0.1.1

Start the Py3o Fusion server:

.. code::

  start-py3o-fusion --debug -s localhost

Start the Py3o render server:

.. code::

  start-py3o-renderserver --java=/usr/lib/jvm/default-java/jre/lib/amd64/server/libjvm.so --ure=/usr/share --office=/usr/lib/libreoffice --driver=juno --sofficeport=8997

On the output of the Py3o render server, the first line looks like:

.. code::

  DEBUG:root:Starting JVM: /usr/lib/jvm/default-java/jre/lib/amd64/server/libjvm.so with options: -Djava.class.path=/usr/local/lib/python2.7/dist-packages/py3o/renderers/juno/py3oconverter.jar:/usr/share/java/juh.jar:/usr/share/java/jurt.jar:/usr/share/java/ridl.jar:/usr/share/java/unoloader.jar:/usr/share/java/java_uno.jar:/usr/lib/libreoffice/program/classes/unoil.jar -Xmx150M

After **-Djava.class.path**, there is a list of Java libs with *.jar* extension ; check that each JAR file is really present on your filesystem. If one of the jar files is present in another directory, create a symlink that points to the real location of the file. If all the jar files are present on another directory, adapt the *--ure=* argument on the command line of Py3o render server.

To check that the Py3o Fusion server is running fine, visit the URL http://<IP_address>:8765/form. On this web page, under the section *Target format*, make sure that you have a line *This server currently supports these formats: ods, odt, docx, doc, html, docbook, pdf, xls.*.

If you want to produce valid PDF/A documents with this module, activating the corresponding option in the PDF Export Options may not be enough, you also have to make sure that all the fonts used in the document template are installed on the Odoo server, so that they can be embedded in the PDF/A document. For example, if your document template uses the Arial font, you should install that font on your Odoo server:

.. code::

  sudo apt-get install msttcorefonts


Known issues / Roadmap
======================

* Add support for PDF signatures (possible, but no easy because the signature certificate is a very particular PDF export option)

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/reporting-engine/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Florent Aide (`XCG Consulting <http://odoo.consulting/>`_)
* Laurent Mignon <laurent.mignon@acsone.eu>,
* Alexis de Lattre <alexis.delattre@akretion.com>,
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Omar Casti??eira <omar@comunitea.com>
* Holger Brunn <hbrunn@therp.nl>

Do not contact contributors directly about help with questions or problems concerning this addon, but use the `community mailing list <mailto:community@mail.odoo.com>`_ or the `appropriate specialized mailinglist <https://odoo-community.org/groups>`_ for help, and the bug tracker linked in `Bug Tracker`_ above for technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
