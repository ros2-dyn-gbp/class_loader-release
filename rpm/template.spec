%{?!ros_distro:%global ros_distro rolling}
%global pkg_name class_loader
%global normalized_pkg_name %{lua:return (string.gsub(rpm.expand('%{pkg_name}'), '_', '-'))}

Name:           ros-rolling-class-loader
Version:        2.7.0
Release:        2%{?dist}
Summary:        ROS %{pkg_name} package

License:        BSD
URL:            http://ros.org/wiki/class_loader
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  bloom-rpm-macros
BuildRequires:  cmake

%{?bloom_package}

%description
The class_loader package is a ROS-independent package for loading plugins during
runtime and the foundation of the higher level ROS &quot;pluginlib&quot;
library. class_loader utilizes the host operating system's runtime loader to
open runtime libraries (e.g. .so/.dll files), introspect the library for
exported plugin classes, and allows users to instantiate objects of these
exported classes without the explicit declaration (i.e. header file) for those
classes.


%package devel
Release:        %{release}%{?release_suffix}
Summary:        %{summary}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-runtime%{?_isa} = %{version}-%{release}

%description devel
The class_loader package is a ROS-independent package for loading plugins during
runtime and the foundation of the higher level ROS &quot;pluginlib&quot;
library. class_loader utilizes the host operating system's runtime loader to
open runtime libraries (e.g. .so/.dll files), introspect the library for
exported plugin classes, and allows users to instantiate objects of these
exported classes without the explicit declaration (i.e. header file) for those
classes.


%package runtime
Release:        %{release}
Summary:        %{summary}

%description runtime
The class_loader package is a ROS-independent package for loading plugins during
runtime and the foundation of the higher level ROS &quot;pluginlib&quot;
library. class_loader utilizes the host operating system's runtime loader to
open runtime libraries (e.g. .so/.dll files), introspect the library for
exported plugin classes, and allows users to instantiate objects of these
exported classes without the explicit declaration (i.e. header file) for those
classes.


%prep
%autosetup -p1


%generate_buildrequires
%bloom_buildrequires


%build
%cmake \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="%{bloom_prefix}" \
    -DAMENT_PREFIX_PATH="%{bloom_prefix}" \
    -DCMAKE_PREFIX_PATH="%{bloom_prefix}" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif

%cmake3_build


%install
%cmake_install


%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C %{__cmake_builddir} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
CTEST_OUTPUT_ON_FAILURE=1 \
    %cmake_build $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif


%files devel
%ghost %{bloom_prefix}/share/%{pkg_name}/package.xml


%files runtime
%{bloom_prefix}


%changelog
* Thu Mar 21 2024 Geoffrey Biggs <geoff@openrobotics.org> - 2.7.0-2
- Autogenerated by Bloom
