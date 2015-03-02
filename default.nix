with import <nixpkgs> {};
with pkgs.python27Packages; 

let

  billiard = pythonPackages.buildPythonPackage rec {
    name = "billiard-3.3.0.19";

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/b/billiard/billiard-3.3.0.19.tar.gz";
      md5 = "7e473b9da01956ce91a650f99fe8d4ad";
    };

    propagatedBuildInputs = with pythonPackages; [ mock nose unittest2 ];

    meta = with stdenv.lib; {
      homepage = http://github.com/celery/billiard;
      license = licenses.bsd;
    };
  };

  amqp = pythonPackages.buildPythonPackage rec {
    name = "amqp-1.4.6";

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/a/amqp/amqp-1.4.6.tar.gz";
      md5 = "a061581b6864f838bffd62b6a3d0fb9f";
    };

    doCheck = false;

    propagatedBuildInputs = with pythonPackages; [ mock coverage ];

    meta = with stdenv.lib; {
      homepage = http://github.com/celery/py-amqp;
    };
  };

  kombu = pythonPackages.buildPythonPackage rec {
    name = "kombu-3.0.24";

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/k/kombu/kombu-3.0.24.tar.gz";
      md5 = "37c8b5084ac83b8a6f5ff9f157cac0e9";
    };

    propagatedBuildInputs = with pythonPackages; [ amqp anyjson unittest2 nose billiard ];

    meta = with stdenv.lib; {
      homepage = http://kombu.readthedocs.org;
    };
  };

  celery = pythonPackages.buildPythonPackage rec {
    name = "celery-3.1.17";

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/c/celery/celery-3.1.17.tar.gz";
      md5 = "e37f5d93b960bf68fc26c1325f30fd16";
    };

    propagatedBuildInputs = with pythonPackages; [ kombu pytz ];

    meta = with stdenv.lib; {
      homepage = http://celeryproject.org;
      license = licenses.bsd;
    };
  };

  youtube_dl = pythonPackages.buildPythonPackage rec {
    name = "youtube_dl-2014.12.16.2";

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/y/youtube_dl/youtube_dl-2014.12.16.2.tar.gz";
      md5 = "fe6c2e093c40dfb5ed5f7202609f44c6";
    };

    propagatedBuildInputs = with pythonPackages; [  ];

    meta = with stdenv.lib; {
      description = "Small command-line program to download videos from YouTube.com and other video sites.";
      homepage = https://github.com/rg3/youtube-dl;
    };
  };

in

buildPythonPackage {
  name = "jigglypuff";

  propagatedBuildInputs = [ 
    python
    virtualenv
    git
    pyramid
    pyramid_jinja2
    pyramid_debugtoolbar
    waitress
    sqlalchemy
    celery
    zope_sqlalchemy
    mock
    nose
    unittest2
    webtest
    youtube_dl
    ffmpeg
    gunicorn
    raven
  ];

  src = ./.;
}
