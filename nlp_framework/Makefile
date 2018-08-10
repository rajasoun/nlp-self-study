.PHONY: test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  test        run all your tests using nose"

env:
	pip install virtualenv && \
  virtualenv --always-copy .env && \
	. .env/bin/activate && \
	make deps
 
sdist:
	make clean && \
	make env && \
	. .env/bin/activate && \
	python setup.py sdist
 
rpm:
	make sdist && \
	mkdir -p temp/opt/b2b/trinity && \
	cp -R .env temp/opt/b2b/trinity && \
	cp -R ~/nltk_data temp/opt/b2b/trinity && \
	[ -f "dist/tagger-0.1.0.tar.gz" ] && tar xvfp dist/tagger-0.1.0.tar.gz -C temp/opt/b2b/trinity && \
	echo "version : ${APP_VERSION}" > temp/opt/b2b/trinity/trinity.version && \
	fpm -s dir -t rpm -a all -v ${APP_VERSION} -n "trinity" --directories /opt/b2b/trinity --before-install "rpm_build/preinstall.sh" \
          --before-remove "rpm_build/preremoval.sh" --after-install "rpm_build/afterinstall.sh" --after-remove "rpm_build/afterremove.sh"\
          --rpm-user trinity --rpm-group trinity  -C temp opt

deps:
	./requirements.sh
	./nltk_setup.py

clean:
	find . -name '*.pyc' -exec rm -f {} \; && \
  rm -rf temp && \
  rm -rf dist

test:
	make clean && \
	make env && \
	. .env/bin/activate && \
	nosetests -s --with-xunit --rednose --force-color

test-summary:
	make clean && \
	nosetests -s --with-xunit tests/summary --rednose --force-color

test-tagger:
	make clean && \
	nosetests -s --with-xunit tests/tagger --rednose --force-color

run-tagger:
	make clean && \
	python run -c config/sample.yml
