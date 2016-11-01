#!/bin/bash
set -e
set -i
set -x

cd $WORKSPACE

STAGING_TMPDIR=`mktemp -d`
GIT_CLONE=`mktemp -d`
PLUGIN='vidi_urls'
NAME="${PLUGIN}-plugin"
LAST_COMMIT=`git rev-parse --short HEAD`
VERSION=`date '+%Y%m%d%H%M'`
PACKAGER='alex@nmr.com'
URL='http://www.nmr.com/'
REQUIRES='python'
SUMMARY="${PLUGIN} lugin ${LAST_COMMIT}"
DESCRIPTION="${SUMMARY}"
BUILD_ARCH=`uname -m`
RHEL_DIST=`/usr/lib/rpm/redhat/dist.sh`
RELEASE="${LAST_COMMIT}${RHEL_DIST}"
GROUP='Applications/Multimedia'
LICENSE='Python'
PKGROOT="${STAGING_TMPDIR}/rpm-staging/RPMBUILD/BUILDROOT/${NAME}-${VERSION}-${RELEASE}.${BUILD_ARCH}"
SPECS="${STAGING_TMPDIR}/rpm-staging/RPMBUILD/SPECS/${NAME}.spec"
STAGING_RPM="${STAGING_TMPDIR}/rpm-staging/RPMBUILD/RPMS/${BUILD_ARCH}/${NAME}-${VERSION}-${RELEASE}.${BUILD_ARCH}.rpm"
OUTPUT_RPM_DIR="${WORKSPACE}/rpm/${BUILD_ARCH}/${RHEL_DIST#.}"
PORTAL_BASEDIR="/opt/cantemo/portal"
PLUGIN_DIR="${PKGROOT}/opt/cantemo/portal/portal/plugins"
INSTALL_LOG="/var/log/cantemo/portal/${NAME}_install_${VERSION}.log"

#Checkout code
git clone "${WORKSPACE}" "${GIT_CLONE}"


# Create build dirs
mkdir -p "${STAGING_TMPDIR}/rpm-staging/RPMBUILD/SPECS"
mkdir -p "${PLUGIN_DIR}"

# Copy plugins
cp -a "${GIT_CLONE}/${PLUGIN}" "${PLUGIN_DIR}/"

find "${PLUGIN_DIR}" -type f -exec chmod 644 {} \;



#Create spec file
echo "Summary: ${SUMMARY}" > "${SPECS}"
echo "License: ${LICENSE}" >> "${SPECS}"
echo "Name: ${NAME}" >> "${SPECS}"
echo "Version: ${VERSION}" >> "${SPECS}"
echo "Release: ${RELEASE}" >> "${SPECS}"
echo "Group: ${GROUP}" >> "${SPECS}"
echo "URL: ${URL}" >> "${SPECS}"
echo "Packager: ${PACKAGER}" >> "${SPECS}"
echo "BuildArch: ${BUILD_ARCH}" >> "${SPECS}"
# echo "Requires: ${REQUIRES}" >> "${SPECS}"
echo "AutoReq: no" >> "${SPECS}"
echo '' >> "${SPECS}"
echo '%description' >> "${SPECS}"
echo "${DESCRIPTION}" >> "${SPECS}"
echo '' >> "${SPECS}"
echo '%files' >> "${SPECS}"
echo '%defattr(-,root,root)' >> "${SPECS}"
(cd "${PKGROOT}" ; find opt/ -type f -printf '/%p\n' ) >> "${SPECS}"
echo '' >> "${SPECS}"

# Set post install script
echo '%posttrans' >> "${SPECS}"
echo "( supervisorctl stop all )" >> "${SPECS}"
while read -r line;
do
  echo "( ${line} >> ${INSTALL_LOG} 2>&1 )" >> "${SPECS}"
done < ${WORKSPACE}/install.sh

echo "( supervisorctl start all )" >> "${SPECS}"
echo "( service memcached restart )" >> "${SPECS}"

# Set post uninstall script
echo '%postun' >> "${SPECS}"
echo "( supervisorctl restart all )" >> "${SPECS}"
echo "( service memcached restart )" >> "${SPECS}"

# build package
echo "Building package"
rpmbuild --target "${BUILD_ARCH}-redhat-linux" --define "_topdir ${STAGING_TMPDIR}/rpm-staging/RPMBUILD" -ba  "${SPECS}"

# Grab output rpm
mkdir -p "${OUTPUT_RPM_DIR}"
mv "${STAGING_RPM}" "${OUTPUT_RPM_DIR}"
