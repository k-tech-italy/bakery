
# Selenium
Download chromedriver from https://googlechromelabs.github.io/chrome-for-testing/



```shell
export DRIVER_VERSION=$(google-chrome --version | grep -iE "[0-9.]{10,20}" | cut -d " " -f 3)
mkdir -p ~webdrivers && curl https://storage.googleapis.com/chrome-for-testing-public/${DRIVER_VERSION}/linux64/chrome-linux64.zip -o ~webdrivers/chrome-linux64.zip
cd ~webdrivers && unzip chrome-linux64 && cd -
```