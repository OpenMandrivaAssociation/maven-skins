%global app_version 1.0-SNAPSHOT
%global def_version 1.1-SNAPSHOT
%global cla_version 1.1-SNAPSHOT
%global sty_version 1.2-SNAPSHOT

Name:           maven-skins
Version:        5
Release:        5
Summary:        Maven Skins

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/skins/
# svn export http://svn.apache.org/repos/asf/maven/skins/tags/maven-skins-5
# tar caf maven-skins-5-tar.xz maven-skins-5/
Source0:        %{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires:  maven2
BuildRequires:  maven-install-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-site-plugin
Requires:       jpackage-utils
Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils
Requires:       java

%description
Skins for the maven site generator. 

%prep
%setup -q 

sed -i -e "s|5-SNAPSHOT|5|g" maven-application-skin/pom.xml
sed -i -e "s|5-SNAPSHOT|5|g" maven-default-skin/pom.xml
sed -i -e "s|5-SNAPSHOT|5|g" maven-classic-skin/pom.xml
sed -i -e "s|5-SNAPSHOT|5|g" maven-stylus-skin/pom.xml
rm -fr src/site/site.xml

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{name}
install -m 644 maven-application-skin/target/maven-application-skin-%{app_version}.jar   %{buildroot}%{_javadir}/%{name}/maven-application-skin-%{app_version}.jar
install -m 644 maven-default-skin/target/maven-default-skin-%{def_version}.jar   %{buildroot}%{_javadir}/%{name}/maven-default-skin-%{def_version}.jar
install -m 644 maven-classic-skin/target/maven-classic-skin-%{cla_version}.jar   %{buildroot}%{_javadir}/%{name}/maven-classic-skin-%{cla_version}.jar
install -m 644 maven-stylus-skin/target/maven-stylus-skin-%{sty_version}.jar   %{buildroot}%{_javadir}/%{name}/maven-stylus-skin-%{sty_version}.jar

(cd %{buildroot}%{_javadir}/%{name} && for jar in *-SNAPSHOT*; \
    do ln -sf ${jar} `echo $jar| sed "s|-[0-9].[0-9]-SNAPSHOT||g"`; done)


# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.maven.skins maven-skins %{version} JPP maven-skins
install -pm 644 maven-application-skin/pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-maven-application-skin.pom
%add_to_maven_depmap org.apache.maven.skins maven-application-skin %{version} JPP/maven-skins maven-application-skin
install -pm 644 maven-default-skin/pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-maven-default-skin.pom
%add_to_maven_depmap org.apache.maven.skins maven-default-skin %{version} JPP/maven-skins maven-default-skin
install -pm 644 maven-classic-skin/pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-maven-classic-skin.pom
%add_to_maven_depmap org.apache.maven.skins maven-classic-skin %{version} JPP/maven-skins maven-classic-skin
install -pm 644 maven-stylus-skin/pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-maven-stylus-skin.pom
%add_to_maven_depmap org.apache.maven.skins maven-stylus-skin %{version} JPP/maven-skins maven-stylus-skin

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

