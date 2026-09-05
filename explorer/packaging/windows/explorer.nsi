Unicode True
RequestExecutionLevel user
SetCompressor /SOLID lzma

!include "MUI2.nsh"
!include "nsDialogs.nsh"
!include "LogicLib.nsh"
!include "FileFunc.nsh"

!ifndef APP_VERSION
  !error "APP_VERSION is required"
!endif
!ifndef FROZEN_DIR
  !error "FROZEN_DIR is required"
!endif
!ifndef OUTPUT_DIR
  !error "OUTPUT_DIR is required"
!endif
!ifndef APP_ICON
  !error "APP_ICON is required"
!endif
!ifdef SIGNTOOL_PATH
  !ifndef SIGN_CERTIFICATE_THUMBPRINT
    !error "SIGN_CERTIFICATE_THUMBPRINT is required when signing"
  !endif
  !ifndef SIGN_TIMESTAMP_URL
    !error "SIGN_TIMESTAMP_URL is required when signing"
  !endif
  !finalize '"${SIGNTOOL_PATH}" sign /sha1 ${SIGN_CERTIFICATE_THUMBPRINT} /fd SHA256 /tr "${SIGN_TIMESTAMP_URL}" /td SHA256 "%1"' = 0
  !uninstfinalize '"${SIGNTOOL_PATH}" sign /sha1 ${SIGN_CERTIFICATE_THUMBPRINT} /fd SHA256 /tr "${SIGN_TIMESTAMP_URL}" /td SHA256 "%1"' = 0
!endif

!ifndef APP_NAME
  !define APP_NAME "MarkdownLLM Explorer"
!endif
!ifndef APP_REGISTRY
  !define APP_REGISTRY "Software\MarkdownLLM Explorer"
!endif
!ifndef UNINSTALL_REGISTRY
  !define UNINSTALL_REGISTRY "Software\Microsoft\Windows\CurrentVersion\Uninstall\MarkdownLLM Explorer"
!endif
!ifndef OUTPUT_NAME
  !define OUTPUT_NAME "MarkdownLLM-Explorer-Installer-${APP_VERSION}.exe"
!endif

Name "${APP_NAME}"
Caption "${APP_NAME} Setup"
OutFile "${OUTPUT_DIR}\${OUTPUT_NAME}"
InstallDir "$LOCALAPPDATA\Programs\${APP_NAME}"
InstallDirRegKey HKCU "${APP_REGISTRY}" "InstallDir"
Icon "${APP_ICON}"
UninstallIcon "${APP_ICON}"
BrandingText "MarkdownLLM"
ShowInstDetails nevershow
ShowUninstDetails nevershow

Var SubstrateRoot
Var RootInput

!define MUI_ABORTWARNING
!define MUI_ICON "${APP_ICON}"
!define MUI_UNICON "${APP_ICON}"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Open ${APP_NAME}"
!define MUI_FINISHPAGE_RUN_FUNCTION LaunchExplorer

!insertmacro MUI_PAGE_WELCOME
Page custom RootPageCreate RootPageLeave
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Function .onInit
  SetShellVarContext current
  ${GetParameters} $0
  ClearErrors
  ${GetOptions} $0 "/SUBSTRATEROOT=" $SubstrateRoot
  ${If} ${Errors}
    ReadRegStr $SubstrateRoot HKCU "${APP_REGISTRY}" "SubstrateRoot"
  ${EndIf}

  ${If} $SubstrateRoot == ""
    ${GetParent} "$EXEDIR" $0
    ${GetParent} "$0" $1
    ${If} ${FileExists} "$1\AGENTS.md"
      StrCpy $SubstrateRoot "$1"
    ${EndIf}
  ${EndIf}

  ${If} ${Silent}
    ${IfNot} ${FileExists} "$SubstrateRoot\AGENTS.md"
      SetErrorLevel 2
      Quit
    ${EndIf}
  ${EndIf}
FunctionEnd

Function un.onInit
  SetShellVarContext current
FunctionEnd

Function RootPageCreate
  nsDialogs::Create 1018
  Pop $0
  ${If} $0 == error
    Abort
  ${EndIf}

  ${NSD_CreateLabel} 0 0 100% 28u "Choose the MarkdownLLM substrate to explore. This is the folder containing its top-level AGENTS.md file."
  Pop $0
  ${NSD_CreateDirRequest} 0 38u 78% 12u "$SubstrateRoot"
  Pop $RootInput
  ${NSD_CreateBrowseButton} 80% 37u 20% 14u "Browse..."
  Pop $0
  ${NSD_OnClick} $0 RootBrowse
  nsDialogs::Show
FunctionEnd

Function RootBrowse
  nsDialogs::SelectFolderDialog "Choose the MarkdownLLM substrate" "$SubstrateRoot"
  Pop $0
  ${If} $0 != error
    ${NSD_SetText} $RootInput "$0"
  ${EndIf}
FunctionEnd

Function RootPageLeave
  ${NSD_GetText} $RootInput $SubstrateRoot
  ${IfNot} ${FileExists} "$SubstrateRoot\AGENTS.md"
    MessageBox MB_ICONEXCLAMATION|MB_OK "That folder is not a MarkdownLLM substrate. Choose the folder containing AGENTS.md."
    Abort
  ${EndIf}
FunctionEnd

Function LaunchExplorer
  ExecShell "open" "$INSTDIR\MarkdownLLM Explorer.exe" '--root "$SubstrateRoot"'
FunctionEnd

Section "Install" SEC_INSTALL
  ${IfNot} ${FileExists} "$SubstrateRoot\AGENTS.md"
    SetErrorLevel 2
    Abort
  ${EndIf}

  IfFileExists "$INSTDIR\MarkdownLLM Explorer.exe" 0 stopped_for_install
    ; The currently installed binary may predate termination acknowledgement.
    ; Run the new payload from NSIS's private directory so an upgrade waits for
    ; the old primary process before touching its files.
    InitPluginsDir
    SetOutPath "$PLUGINSDIR\ExplorerStop"
    File /r "${FROZEN_DIR}\*.*"
    ExecWait '"$PLUGINSDIR\ExplorerStop\MarkdownLLM Explorer.exe" --request-exit --root "$SubstrateRoot"' $0
  ${If} $0 != 0
    SetErrorLevel 4
    Abort
  ${EndIf}
  stopped_for_install:

  RMDir /r "$INSTDIR\_internal"
  Delete "$INSTDIR\MarkdownLLM Explorer.exe"
  SetOutPath "$INSTDIR"
  File /r "${FROZEN_DIR}\*.*"
  ; A versioned icon path avoids reusing the shell's cached pre-branding icon.
  File /oname=brand-icon-${APP_VERSION}.ico "${APP_ICON}"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  WriteRegStr HKCU "${APP_REGISTRY}" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "${APP_REGISTRY}" "SubstrateRoot" "$SubstrateRoot"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "Publisher" "MarkdownLLM"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "DisplayIcon" "$INSTDIR\brand-icon-${APP_VERSION}.ico"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
  WriteRegDWORD HKCU "${UNINSTALL_REGISTRY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINSTALL_REGISTRY}" "NoRepair" 1

  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\MarkdownLLM Explorer.exe" '--root "$SubstrateRoot"' "$INSTDIR\brand-icon-${APP_VERSION}.ico" 0 SW_SHOWNORMAL "" "Explore this MarkdownLLM substrate"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\MarkdownLLM Explorer.exe" '--root "$SubstrateRoot"' "$INSTDIR\brand-icon-${APP_VERSION}.ico" 0 SW_SHOWNORMAL "" "Explore this MarkdownLLM substrate"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  IfFileExists "$INSTDIR\MarkdownLLM Explorer.exe" 0 stopped_for_uninstall
    ExecWait '"$INSTDIR\MarkdownLLM Explorer.exe" --request-exit --root "$INSTDIR"' $0
  ${If} $0 != 0
    SetErrorLevel 4
    Abort
  ${EndIf}
  stopped_for_uninstall:

  Delete "$DESKTOP\${APP_NAME}.lnk"
  RMDir /r "$SMPROGRAMS\${APP_NAME}"
  DeleteRegKey HKCU "${UNINSTALL_REGISTRY}"
  DeleteRegKey HKCU "${APP_REGISTRY}"
  RMDir /r "$INSTDIR"
SectionEnd
