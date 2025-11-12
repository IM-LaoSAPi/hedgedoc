# NASA HW8

### 資管二 B13705020 陳鼎元

## 1 Server setup
在Server端VM設定
```bash!
apt update

# 安裝 OpenLDAP
apt install -y slapd ldap-utils

# 配置 SLAPD
dpkg-reconfigure slapd
```
創建 LDIF 檔案
```bash!
nano /root/base.ldif
```
```nginx!
dn: ou=people,dc=nasa,dc=csie,dc=ntu
objectClass: organizationalUnit
ou: people

dn: ou=group,dc=nasa,dc=csie,dc=ntu
objectClass: organizationalUnit
ou: group
```
```bash!
# 匯入
ldapadd -x -D "cn=admin,dc=nasa,dc=csie,dc=ntu" -W -f /root/base.ldif
```
![image](https://hackmd.io/_uploads/B1ZjWXRybx.png)


## 2 Client Setup
```bash!
# 安裝 OpenLDAP 客戶端工具
pacman -Sy --noconfirm openldap
```
```bash!
vim /etc/openldap/ldap.conf

### 調整以下
   BASE    dc=nasa,dc=csie,dc=ntu
   URI     ldap://192.168.8.1
```
![image](https://hackmd.io/_uploads/HyLTzXRJWx.png)

## 3 LDAPS

### (a)
```bash!
# 安裝工具
apt install -y gnutls-bin

# 創建憑證目錄
mkdir -p /etc/ldap/ssl
cd /etc/ldap/ssl

# 產生 CA 私鑰
certtool --generate-privkey --outfile ca-key.pem

# CA 憑證範本
cat > ca.info << 'EOF'
cn = NASA LDAP CA
ca
cert_signing_key
expiration_days = 3650
EOF

# 產生 CA 憑證
certtool --generate-self-signed \
  --load-privkey ca-key.pem \
  --template ca.info \
  --outfile ca-cert.pem
  
# 產生伺服器私鑰
certtool --generate-privkey --outfile ldap-key.pem

# 創建伺服器憑證範本
cat > ldap.info << 'EOF'
organization = NASA CSIE NTU
cn = 192.168.8.1
tls_www_server
encryption_key
signing_key
expiration_days = 3650
EOF

# 產生伺服器憑證
certtool --generate-certificate \
  --load-privkey ldap-key.pem \
  --load-ca-certificate ca-cert.pem \
  --load-ca-privkey ca-key.pem \
  --template ldap.info \
  --outfile ldap-cert.pem

# 檔案權限
chown openldap:openldap /etc/ldap/ssl/*.pem
chmod 600 /etc/ldap/ssl/*-key.pem
chmod 644 /etc/ldap/ssl/ca-cert.pem
chmod 644 /etc/ldap/ssl/ldap-cert.pem

```
```bash!
# 配置 LDAP 使用 TLS
nano /root/tls.ldif
```
    dn: cn=config
    changetype: modify
    add: olcTLSCACertificateFile
    olcTLSCACertificateFile: /etc/ldap/ssl/ca-cert.pem
    -
    add: olcTLSCertificateFile
    olcTLSCertificateFile: /etc/ldap/ssl/ldap-cert.pem
    -
    add: olcTLSCertificateKeyFile
    olcTLSCertificateKeyFile: /etc/ldap/ssl/ldap-key.pem
```bash!
# 匯入 TLS 配置
ldapmodify -Y EXTERNAL -H ldapi:/// -f /root/tls.ldif
```
```bash!
nano /etc/ldap/ldap.conf

# 修改以下
TLS_CACERT /etc/ldap/ssl/ca-cert.pem
TLS_REQCERT allow
```
```bash!
nano /etc/default/slapd

# 修改以下
SLAPD_SERVICES="ldap:/// ldapi:/// ldaps:///"
```
```bash!
systemctl restart slapd
systemctl status slapd
```

### (b)
![image](https://hackmd.io/_uploads/SJai9m01-e.png)

### \(c)
![image](https://hackmd.io/_uploads/BJ2a9X0Jbe.png)

### (d)
```bash!
nano /root/force-tls.ldif 
```
```bash!
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcSecurity
olcSecurity: tls=1
```
匯入設定
```bash!
ldapmodify -Y EXTERNAL -H ldapi:/// -f /root/force-tls.ldif
```
### (e)
Server 端找出憑證
```bash!
cat /etc/ldap/ssl/ca-cert.pem
```
在 client VM 上創建憑證
```bash!
mkdir -p /etc/openldap/certs
```
```bash!
cat > /etc/openldap/certs/ca-cert.pem << 'EOF'
-----BEGIN CERTIFICATE-----
MIID/jCCAmagAwIBAgIUEg ...
-----END CERTIFICATE-----
EOF
```
修改設定
```bash!
vim /etc/openldap/ldap.conf 
# 加入這兩行
TLS_CACERT /etc/openldap/certs/ca-cert.pem
TLS_REQCERT allow
```
![image](https://hackmd.io/_uploads/SyJLp7RJbg.png)

### (f)
![image](https://hackmd.io/_uploads/H1QFaXCJ-e.png)



## 4 

### 創建群組及使用者

```bash!
cat > /root/groups.ldif << 'EOF'
dn: cn=ta,ou=group,dc=nasa,dc=csie,dc=ntu
objectClass: posixGroup
cn: ta
gidNumber: 10001

dn: cn=student,ou=group,dc=nasa,dc=csie,dc=ntu
objectClass: posixGroup
cn: student
gidNumber: 10002
EOF
```
匯入群組
```bash!
ldapadd -x -ZZ -D "cn=admin,dc=nasa,dc=csie,dc=ntu" -W -f /root/groups.ldif
```

```bash!
# ta
slappasswd
{SSHA}6M79iBrP5tuin0LM956tB2+5NI1KI8wm
# student
slappasswd
{SSHA}KZagpb0kq93bl5BYRt59QKBDaZSWyzrV
```
```bash!
cat > /root/users.ldif << 'EOF'
dn: uid=ta001,ou=people,dc=nasa,dc=csie,dc=ntu
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: ta001
sn: TA
givenName: Teaching
cn: Teaching Assistant
displayName: TA 001
uidNumber: 20001
gidNumber: 10001
userPassword: {SSHA}6M79iBrP5tuin0LM956tB2+5NI1KI8wm
loginShell: /bin/bash
homeDirectory: /home/ta001
mail: ta001@nasa.csie.ntu

dn: uid=student001,ou=people,dc=nasa,dc=csie,dc=ntu
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: student001
sn: Student
givenName: Normal
cn: Normal Student
displayName: Student 001
uidNumber: 20002
gidNumber: 10002
userPassword: {SSHA}KZagpb0kq93bl5BYRt59QKBDaZSWyzrV
loginShell: /bin/bash
homeDirectory: /home/student001
mail: student001@nasa.csie.ntu
EOF
```
匯入使用者：
```bash!
ldapadd -x -ZZ -D "cn=admin,dc=nasa,dc=csie,dc=ntu" -W -f /root/users.ldif
```

### sudo 規則
在 Server VM 上：
```bash!
cat > /root/sudo-schema.ldif << 'EOF'
dn: cn=sudo,cn=schema,cn=config
objectClass: olcSchemaConfig
cn: sudo
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.1 NAME 'sudoUser' DESC 'User(s) who may run sudo' EQUALITY caseExactMatch SUBSTR caseExactSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.2 NAME 'sudoHost' DESC 'Host(s) who may run sudo' EQUALITY caseExactMatch SUBSTR caseExactSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.3 NAME 'sudoCommand' DESC 'Command(s) to be executed by sudo' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.4 NAME 'sudoRunAs' DESC 'User(s) impersonated by sudo' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.5 NAME 'sudoOption' DESC 'Options(s) followed by sudo' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.6 NAME 'sudoRunAsUser' DESC 'User(s) impersonated by sudo' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.7 NAME 'sudoRunAsGroup' DESC 'Group(s) impersonated by sudo' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.8 NAME 'sudoNotBefore' DESC 'Start of time interval for sudoers entry' EQUALITY generalizedTimeMatch ORDERING generalizedTimeOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.9 NAME 'sudoNotAfter' DESC 'End of time interval for sudoers entry' EQUALITY generalizedTimeMatch ORDERING generalizedTimeOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.10 NAME 'sudoOrder' DESC 'Ordering of sudoers entries' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 )
olcObjectClasses: ( 1.3.6.1.4.1.15953.9.2.1 NAME 'sudoRole' DESC 'Sudoers Role' SUP top STRUCTURAL MUST cn MAY ( sudoUser $ sudoHost $ sudoCommand $ sudoRunAs $ sudoRunAsUser $ sudoRunAsGroup $ sudoOption $ sudoOrder $ sudoNotBefore $ sudoNotAfter $ description ) )
EOF
```
匯入
```bash!
ldapadd -Y EXTERNAL -H ldapi:/// -f /root/sudo-schema.ldif
```
TA 加入 sudo
```bash!
cat > /root/sudo-rules.ldif << 'EOF'
dn: ou=sudoers,dc=nasa,dc=csie,dc=ntu
objectClass: organizationalUnit
ou: sudoers

dn: cn=ta-sudo,ou=sudoers,dc=nasa,dc=csie,dc=ntu
objectClass: sudoRole
cn: ta-sudo
sudoUser: %ta
sudoHost: ALL
sudoCommand: ALL
sudoRunAsUser: ALL
EOF
```
匯入
```bash!
ldapadd -x -D "cn=admin,dc=nasa,dc=csie,dc=ntu" -W -f /root/sudo-rules.ldif
```

### 在 Client 安裝和設定 SSSD
安裝套件
```bash!
pacman -Sy --noconfirm sssd sudo
```
建立 `/etc/sssd/sssd.conf`
```bash!
cat > /etc/sssd/sssd.conf << 'EOF'
[sssd]
services = nss, pam, sudo
config_file_version = 2
domains = nasa.csie.ntu

[domain/nasa.csie.ntu]
id_provider = ldap
auth_provider = ldap
sudo_provider = ldap
ldap_uri = ldaps://192.168.8.1
ldap_search_base = dc=nasa,dc=csie,dc=ntu
ldap_sudo_search_base = ou=sudoers,dc=nasa,dc=csie,dc=ntu
ldap_tls_cacert = /etc/openldap/certs/ca-cert.pem
ldap_tls_reqcert = allow
enumerate = True
cache_credentials = True
EOF

chmod 600 /etc/sssd/sssd.conf
```
修改 `/etc/nsswitch.conf`
```bash!
passwd: files sss
group: files sss
shadow: files sss
sudoers: files sss
hosts: files dns
```
設定 PAM (system-auth)
```bash!
cat > /etc/pam.d/system-auth << 'EOF'
#%PAM-1.0

auth       sufficient                  pam_sss.so          forward_pass
auth       required                    pam_unix.so         try_first_pass nullok
auth       optional                    pam_permit.so

account    sufficient                  pam_sss.so
account    required                    pam_unix.so
account    optional                    pam_permit.so

password   sufficient                  pam_sss.so          use_authtok
password   required                    pam_unix.so         try_first_pass nullok sha512 shadow
password   optional                    pam_permit.so

session    optional                    pam_keyinit.so      revoke
session    required                    pam_limits.so
session    required                    pam_unix.so
session    optional                    pam_sss.so
session    required                    pam_mkhomedir.so    skel=/etc/skel umask=0077
EOF
```
同時修改 sshd 專用的 PAM
```bash!
cat > /etc/pam.d/sshd << 'EOF'
#%PAM-1.0

auth       include      system-remote-login
account    include      system-remote-login
password   include      system-remote-login
session    include      system-remote-login
```
system-remote-login
```bash!
cat > /etc/pam.d/system-remote-login << 'EOF'
#%PAM-1.0

auth       sufficient   pam_sss.so       forward_pass
auth       include      system-login

account    sufficient   pam_sss.so
account    include      system-login

password   include      system-login

session    optional     pam_loginuid.so
session    include      system-login
session    optional     pam_mkhomedir.so skel=/etc/skel umask=0077
EOF
```
system-login
```bash!
cat > /etc/pam.d/system-login << 'EOF'
#%PAM-1.0

auth       required     pam_tally2.so        onerr=succeed file=/var/log/tallylog
auth       required     pam_shells.so
auth       requisite    pam_nologin.so
auth       sufficient   pam_sss.so
auth       required     pam_unix.so          try_first_pass nullok

account    required     pam_access.so
account    required     pam_nologin.so
account    sufficient   pam_sss.so
account    required     pam_unix.so
account    required     pam_permit.so

password   sufficient   pam_sss.so           use_authtok
password   required     pam_unix.so          try_first_pass nullok sha512 shadow

session    required     pam_limits.so
session    required     pam_unix.so
session    optional     pam_sss.so
session    optional     pam_mkhomedir.so     skel=/etc/skel umask=0077
EOF
```
重啟
```bash!
systemctl restart sshd
```
![image](https://hackmd.io/_uploads/ryyAWSR1Wl.png)
![image](https://hackmd.io/_uploads/ryYkzHR1Wx.png)


## 5
新的 ACL 規則
```
nano /root/acl.ldif 
```
```bash!
dn: olcDatabase={1}mdb,cn=config
changetype: modify
delete: olcAccess
-
add: olcAccess
olcAccess: {0}to attrs=userPassword
  by self write
  by anonymous auth
  by * none
-
add: olcAccess
olcAccess: {1}to attrs=cn,uid,uidNumber,gidNumber,homeDirectory
  by self read
  by * read
-
add: olcAccess
olcAccess: {2}to *
  by self write
  by users read
  by anonymous read
```

> **規則 0 (userPassword):**
> - `by self write` - 使用者可以修改自己的密碼
> - `by anonymous auth` - 匿名用戶可以用來認證
> - `by * none` - 其他人完全不能讀取
> 
> **規則 1 (不可修改的屬性):**
> - `by self read` - 使用者只能讀取自己的這些屬性
> - `by * read` - 其他人可以讀取
> 
> **規則 2 (其他所有屬性):**
> - `by self write` - 使用者可以修改自己的
> - `by users read` - 已認證使用者可以讀取
> - `by anonymous read` - 匿名也可以讀取

匯入
```bash!
ldapmodify -Y EXTERNAL -H ldapi:/// -f /root/acl.ldif
```

### (a)
以 ta001 身份嘗試修改 student001，失敗
![image](https://hackmd.io/_uploads/SJHbXSA1-l.png)

### (b)
修改允許的屬性（loginShell）- 成功
![image](https://hackmd.io/_uploads/HycZNSA1be.png)
修改受限屬性（uidNumber）- 失敗
![image](https://hackmd.io/_uploads/B1hV4H0ybg.png)

### \(c)
以 ta001 身份讀取 student001 的資料：
![image](https://hackmd.io/_uploads/SJpjESRJ-g.png)
匿名讀取
![image](https://hackmd.io/_uploads/S1eAESRJ-x.png)


## 6

先備份
```bash!
# 停止服務
systemctl stop slapd

# 備份資料庫
cp -r /var/lib/ldap /var/lib/ldap.backup

# 備份設定
cp -r /etc/ldap /etc/ldap.backup

# 重啟服務
systemctl start slapd
```

創建 Schema
```bash!
cat > /root/ntu-student-schema.ldif << 'EOF'
dn: cn=ntustudent,cn=schema,cn=config
objectClass: olcSchemaConfig
cn: ntustudent
olcAttributeTypes: ( 1.3.6.1.4.1.99999.1.1.1
  NAME 'studentEntryMethod'
  DESC 'Student entry method to NTU'
  EQUALITY caseIgnoreMatch
  SUBSTR caseIgnoreSubstringsMatch
  SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
  SINGLE-VALUE )
olcAttributeTypes: ( 1.3.6.1.4.1.99999.1.1.2
  NAME 'studentAdvisor'
  DESC 'Student advisor name'
  EQUALITY caseIgnoreMatch
  SUBSTR caseIgnoreSubstringsMatch
  SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
  SINGLE-VALUE )
olcAttributeTypes: ( 1.3.6.1.4.1.99999.1.1.3
  NAME 'studentClub'
  DESC 'Student club membership'
  EQUALITY caseIgnoreMatch
  SUBSTR caseIgnoreSubstringsMatch
  SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcObjectClasses: ( 1.3.6.1.4.1.99999.1.2.1
  NAME 'ntuStudent'
  DESC 'NTU Student'
  SUP top
  AUXILIARY
  MUST ( studentEntryMethod $ studentAdvisor )
  MAY ( studentClub ) )
EOF
```


> **定義：**
> 1. `studentEntryMethod` - 入學管道（必要）
> 2. `studentAdvisor` - 導師（必要）
> 3. `studentClub` - 社團（可選，可多個）
> 
> **objectClass：**
> - `ntuStudent` - AUXILIARY 類型（輔助類型，可以加到現有使用者上）
> - MUST：必須有 studentEntryMethod 和 studentAdvisor
> - MAY：可以有多個 studentClub


匯入
```bash!
ldapadd -Y EXTERNAL -H ldapi:/// -f /root/ntu-student-schema.ldif
```

### 創建使用者
雜湊密碼
```bash!
STUDENT_PASS=$(slappasswd -s student002pass)
echo "Student002 password hash: $STUDENT_PASS"
```

創建使用者資訊
```bash
cat > /root/ntu-student-user.ldif << EOF
dn: uid=student002,ou=people,dc=nasa,dc=csie,dc=ntu
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
objectClass: ntuStudent
uid: student002
sn: Chen
givenName: Tim 
cn: Chen Tim
displayName: Student 002
uidNumber: 20003
gidNumber: 10002
userPassword: $STUDENT_PASS
loginShell: /bin/bash
homeDirectory: /home/student002
mail: student002@nasa.csie.ntu
studentEntryMethod: self_apply
studentAdvisor: hsinmu
studentClub: aiclub
studentClub: imclub
EOF
```
匯入
```bash!
ldapadd -x -ZZ -D "cn=admin,dc=nasa,dc=csie,dc=ntu" -W -f /root/ntu-student-user.ldif
```

![image](https://hackmd.io/_uploads/rJTBFBR1Zg.png)
