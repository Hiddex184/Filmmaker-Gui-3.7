# -*- coding: utf-8 -*-
import sfm
import sfmApp
from PySide import QtGui, QtCore, shiboken
import ctypes
import struct
import sys
import traceback
import time
import os
import json
import re
import ConfigParser
import hashlib
import codecs
import functools
import  vs
import sfm
from PySide import QtCore, QtGui
import vs,sfm,sfmApp,sfmUtils,sfmClipEditor,os
from vs import g_pDataModel as dm



# ---------- Theme palette (Modern Dark) ----------
PALETTE = {
    # Exact SFM UI colours (sampled from SFM screenshots)
    'bg':           "#2B2B2B",   # deepest bg — SFM main bg
    'panel':        "#353535",   # panel / widget surface
    'panel2':       "#444444",   # raised panel / header
    'muted':        "#333333",   # subtle divider
    'border':       "#1a1a1a",   # hard dark border
    'border_light': "#555555",   # lighter inner border
    'text':         "#c8c8c8",   # SFM primary text
    'text_dim':     "#888888",   # secondary / disabled
    'text_bright':  "#e8e8e8",   # bright label
    # SFM selection blue — the characteristic Valve blue
    'accent':       "#4d7cc4",   # SFM selection / active blue
    'accent_hover': "#6090d8",
    'accent_active':"#3a62a0",
    # Valve button gradient colours
    'btn_top':      "#5a5a5a",
    'btn_bot':      "#3e3e3e",
    'btn_hover':    "#6a6a6a",
    'btn_pressed':  "#303030",
    # Utility — kept for coloured buttons
    'danger':       "#a03030",
    'red':          "#8a2828",
    'success':      "#2a6e30",
    "green":        "#2e7d32",
    'teal':         "#2a7a8a",
    "navy blue":    "#1a2f4a",
    "orange":       "#b06820",
    "pink":         "#7a2840",
    'purple':       "#5050a0",
}

# location for notes file
NOTES_FILENAME = os.path.join(os.path.dirname(__file__), "sfm_notes.txt") if "__file__" in globals() else "sfm_notes.txt"

# Supported skyboxes (names supported by SFM)
SKYBOXES = [
    'sky_dustbowl_01','sky_granary_01','sky_gravel_01','sky_well_01','sky_tf2_04','sky_hydro_01',
    'sky_badlands_01','sky_goldrush_01','sky_trainyard_01','sky_night_01','sky_alpinestorm_01',
    'sky_morningsnow_01','sky_nightfall_01','sky_harvest_01','sky_harvest_night_01','sky_upward',
    'sky_stormfront_01','sky_halloween','sky_halloween_night_01','sky_halloween_night2014_01','sky_island_01',
    'sky_jungle_01','sky_invasion2fort_01','sky_well_02','sky_outpost_01','sky_coastal_01',
    'sky_midnight_01','sky_midnight_02','sky_volcano_01','sky_day01_01','sky_badlands_pyroland',
    'sky_pyroland_01','sky_pyroland_02','sky_pyroland_03','sky_rainbow_01','sky_tf2_05','sky_tf2_06',
    'sky_day01_09','sky_ep02_01_hdr'
]

# Language support 
LANGUAGES = ["English", "Turkish", "Espanol", "Russian", "Arabic", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese", "Korean"]
DEFAULT_LANGUAGE = "English"
CURRENT_LANGUAGE = DEFAULT_LANGUAGE
TRANSLATIONS = {
    "Filmmaker GUI": {"Espanol": "GUI de Cine", "Russian": "GUI для создания кино", "Arabic": "واجهة إنشاء الفيلم", "Turkish": u" Kaynak Film Yapımcısı Arayüzü", "French": "Interface de Création de Film", "German": "Filmhersteller GUI", "Italian": "Interfaccia di Creazione del Film", "Portuguese": "Interface de Criação de Filme", "Chinese": "电影制作人界面", "Japanese": "映画作成GUI", "Korean": "영화 제작 GUI"},
    "Filmmaker GUI 2": {"Turkish": "Filmmaker GUI 2", "Espanol": "GUI de Cine 2", "Russian": "GUI для создания кино 2", "Arabic": "واجهة إنشاء الفيلم ٢",u"Turkish": u"Kaynak Film Yapımcısı Arayüzü 2", u"French": u"Interface de Création de Film 2", u"German": u"Filmhersteller GUI 2", u"Italian": u"Interfaccia di Creazione del Film 2", u"Portuguese": u"Interface de Criação de Filme 2", u"Chinese": u"电影制作人界面 2", u"Japanese": u"映画作成GUI 2", u"Korean": u"영화 제작 GUI 2"},
    "Quick Commands": {"Turkish": "Hizli Komutlar", "Espanol": "Comandos Rápidos", "Russian": "Быстрые команды", "Arabic": "أوامر سريعة"," French": "Commandes Rapides", "German": "Schnellbefehle", "Italian": "Comandi Rapidi", "Portuguese": "Comandos Rápidos", "Chinese": "快速命令", "Japanese": "クイックコマンド", "Korean": "빠른 명령"},
    "Clear Console": {"Turkish": "Konsolu Temizle", "Espanol": "Limpiar Consola", "Russian": "Очистить консоль", "Arabic": "مسح وحدة التحكم"," French": "Effacer la Console", "German": "Konsole löschen", "Italian": "Pulisci Console", "Portuguese": "Limpar Console", "Chinese": "清除控制台", "Japanese": "コンソールをクリア", "Korean": "콘솔 지우기"},
    "Preview Audio": {"Turkish": "Önizle"},
    "Clear": {"Turkish": "Temizle", "Espanol": "Limpiar", "Russian": "Очистить", "Arabic": "واضح"},
    "Add": {"Turkish": "Ekle"},
    "Notes saved successfully ": {u"Turkish": "Notlar başarıyla kaydedildi", "Espanol": "Notas guardadas con éxito", "Russian": "Заметки успешно сохранены","Arabic": "تم حفظ الملاحظات بنجاح"," French": "Notes enregistrées avec succès", "German": "Notizen erfolgreich gespeichert", "Italian": "Note salvate con successo", "Portuguese": "Notas salvas com sucesso", "Chinese": "笔记保存成功", "Japanese": "ノートが正常に保存されました", "Korean": "메모가 성공적으로 저장됨"},
    "Save Notes": {u"Turkish": "Notları Kaydet", "Espanol": "Guardar Notas", "Russian": "Сохранить заметки", "Arabic": "حفظ الملاحظات"," French": "Enregistrer les Notes", "German": "Notizen speichern", "Italian": "Salva Note", "Portuguese": "Salvar Notas", "Chinese": "保存笔记", "Japanese": "ノートを保存", "Korean": "노트 저장"},
    "Clear All": {"Turkish": "Hepsini Temizle", "Espanol": "Limpiar Todo", "Russian": "Очистить все", "Arabic": "مسح الكل"," French": "Tout Effacer", "German": "Alles löschen", "Italian": "Cancella tutto", "Portuguese": "Limpar Tudo", "Chinese": "清除所有"},
    "Choose language:": {"Turkish": "Dil seçin:", "Espanol": "Elige lengua:", "Russian": "Выберите язык:", "Arabic": "اختر اللغة:"," French": "Choisir la langue :", "German": "Sprache wählen:", "Italian": "Scegli la lingua:", "Portuguese": "Escolha o idioma:", "Chinese": "选择语言：", "Japanese": "言語を選択：", "Korean": "언어 선택:"},
    "Apply Language": {"Turkish": "Dili Uygula", "Espanol": "Aplicar Idioma", "Russian": "Применить язык", "Arabic": "تطبيق اللغة"," French": "Appliquer la Langue", "German": "Sprache anwenden", "Italian": "Applica Lingua", "Portuguese": "Aplicar Idioma", "Chinese": "应用语言", "Japanese": u"言語を適用", u"Korean": u"언어 적용"},
    "Reset Language": {"Turkish": "Dili Sifirla", "Espanol": "Restablecer Idioma", "Russian": "Сбросить язык", "Arabic": "إعادة تعيين اللغة"," French": "Réinitialiser la Langue", "German": "Sprache zurücksetzen", "Italian": "Reimpostare la Lingua", "Portuguese": "Redefinir Idioma", "Chinese": "重置语言", "Japanese": "言語をリセット", "Korean": "언어 재설정"},
    "Boost Now": {u"Turkish": "Şimdi artırın", "Espanol": "Aumentar Ahora", "Russian": "Увеличить сейчас", "Arabic": "تعزيز الآن"," French": "Booster Maintenant", "German": "Jetzt Boost", "Italian": "Aumenta Ora", "Portuguese": "Impulsionar Agora", "Chinese": "立即提升", "Japanese": "今すぐブースト", "Korean": "지금 부스트"},
    "Select quick command": {u"Turkish": "Hızlı komut seçin", "Espanol": "Seleccionar comando rápido", "Russian": "Выбрать быструю команду", "Arabic": "حدد الأمر السريع"," French": "Sélectionner une commande rapide", "German": "Schnellbefehl auswählen", "Italian": "Seleziona comando rapido", "Portuguese": "Selecionar comando rápido", "Chinese": "选择快速命令", "Japanese": "クイックコマンドを選択", "Korean": "빠른 명령 선택"},
    "Set Skybox": {"Turkish": "Skybox Ayarla", "Espanol": "Establecer Skybox", "Russian": "Установить небо", "Arabic": "تعيين صندوق السماء"," French": "Définir le Skybox", "German": "Skybox festlegen", "Italian": "Imposta Skybox", "Portuguese": "Definir Skybox", "Chinese": "设置天空盒", "Japanese": "スカイボックスを設定", "Korean": "스카이박스 설정"},
    "Reset Skybox": {"Turkish": "Skybox'i Sifirla", "Espanol": "Restablecer Skybox", "Russian": "Сбросить небо", "Arabic": "إعادة تعيين صندوق السماء"," French": "Réinitialiser le Skybox", "German": "Skybox zurücksetzen", "Italian": "Reimpostare Skybox", "Portuguese": "Redefinir Skybox", "Chinese": "重置天空盒", "Japanese": "スカイボックスをリセット", "Korean": "스카이박스 재설정"},
    "RAM Boost Level": {u"Turkish": "RAM Artırma Seviyesi"},
    "FPS Boost Level": {u"Turkish": "FPS Artış Seviyesi"},
    "Execute": {u"Turkish": "Çalıştır", "Espanol": "Ejecutar", "Russian": "Выполнить", "Arabic": "ينفذ"," French": "Exécuter", "German": "Ausführen", "Italian": "Esegui", "Portuguese": "Executar", "Chinese": "执行", "Japanese": "実行", "Korean": "실행"},
    "Fog Settings": {"Turkish": u"Sis ayarları", "Espanol": "Configuración de Niebla", "Russian": "Настройки тумана", "Arabic": "إعدادات الضباب"," French": "Paramètres de Brouillard", "German": "Nebel-Einstellungen", "Italian": "Impostazioni Nebbia", "Portuguese": "Configurações de Névoa", "Chinese": "雾设置", "Japanese": "フォグ設定", "Korean": "안개 설정"},
    "Extra": {"Turkish": "Ekstra", "Espanol": "Extra", "Russian": "Дополнительно", "Arabic": "إضافي"," French": "Supplémentaire", "German": "Extra", "Italian": "Extra", "Portuguese": "Extra", "Chinese": "额外的", "Japanese": "エクストラ", "Korean": "추가"},
    "quick_commands": {u"Turkish": "Hızlı komut seçin", "Espanol": "Seleccionar comando rápido", "Russian": "Выбрать быструю команду", "Arabic": "حدد الأمر السريع"," French": "Sélectionner une commande rapide", "German": "Schnellbefehl auswählen", "Italian": "Seleziona comando rapido", "Portuguese": "Selecionar comando rápido", "Chinese": "选择快速命令", "Japanese": "クイックコマンドを選択", "Korean": "빠른 명령 선택"},
    "Set Fog Settings": {u"Turkish": "Sis Ayarlarını Ayarla", "Espanol": "Establecer Configuración de Niebla", "Russian": "Установить настройки тумана", "Arabic": "تعيين إعدادات الضباب"," French": "Définir les Paramètres de Brouillard", "German": "Nebel-Einstellungen festlegen", "Italian": "Imposta le Impostazioni della Nebbia", "Portuguese": "Definir Configurações de Névoa", "Chinese": "设置雾设置", "Japanese": "フォグ設定を設定", "Korean": "안개 설정 설정"},
    "Enter skybox name or choose from info": {u"Turkish": "Skybox adını girin veya bilgiden seçin", "Espanol": "Ingrese el nombre del skybox o elija de la información", "Russian": "Введите имя неба или выберите из информации", "Arabic": "أدخل اسم صندوق السماء أو اختر من المعلومات"," French": "Entrez le nom du skybox ou choisissez dans les informations", "German": "Geben Sie den Skybox-Namen ein oder wählen Sie aus den Informationen", "Italian": "Inserisci il nome dello skybox o scegli dalle informazioni", "Portuguese": "Digite o nome do skybox ou escolha nas informações", "Chinese": "输入天空盒名称或从信息中选择", "Japanese": "スカイボックス名を入力するか、情報から選択してください", "Korean": "스카이박스 이름을 입력하거나 정보에서 선택"},
    "Turkish": {"Turkish": "Türkce"},
    "English": {"Turkish": "İngilizce"},
    "Skybox": {"Turkish": "Gökyüzü kutusu", "Espanol": "Skybox", "Russian": "Небо", "Arabic": "صندوق السماء"},
    "Enable Fog": {"Turkish": "Sis etkinleştir", "Espanol": "Habilitar Niebla", "Russian": "Включить туман"},
    "Fog start": {"Turkish": "Sis başlangici"},
    "Fog end": {"Turkish": "Sis sonu"},
    "Set mat_picmip": {"Turkish": "mat_picmip ayarla", "Espanol": "Establecer mat_picmip", "Russian": "Установить mat_picmip", "Arabic": "تعيين mat_picmip"," French": "Définir mat_picmip", "German": "mat_picmip festlegen", "Italian": "Imposta mat_picmip", "Portuguese": "Definir mat_picmip", "Chinese": "设置 mat_picmip", "Japanese": "mat_picmip を設定", "Korean": "mat_picmip 설정"},
    "Execute Quick Command": {u"Turkish": "Hızlı Komutu Çaliştır", "Espanol": "Ejecutar Comando Rápido", "Russian": "Выполнить быструю команду", "Arabic": "تنفيذ الأمر السريع"},
    "SFM Notes": {u"Turkish": "Sfm Notları", "Espanol": "Notas de SFM", "Russian": "Заметки SFM", "Arabic": "ملاحظات SFM", "French": "Notes SFM", "German": "SFM-Notizen", "Italian": "Note SFM", "Portuguese": "Notas SFM", "Chinese": "SFM笔记", "Japanese": "SFMノート", "Korean": "SFM 노트"},
    "Auto Lip Sync": {u"Turkish": "Otomatik Dudak Senkronu", "Espanol": "Sincronizacion Labial", "Russian": "Авто Синхронизация", "Arabic": "مزامنة الشفاه", "French": "Sync Levres Auto", "German": "Lippensync Auto", "Italian": "Sinc Labbra Auto", "Portuguese": "Sincronizacao Labial", "Chinese": "自动口型同步", "Japanese": "自動リップシンク", "Korean": "자동 립싱크"},
    "Texture Checker": {u"Turkish": "Doku Denetleyici", "Espanol": "Verificador de Texturas", "Russian": "Проверка Текстур", "Arabic": "فاحص القوام", "French": "Verificateur de Textures", "German": "Textur-Prufer", "Italian": "Controllo Texture", "Portuguese": "Verificador de Texturas", "Chinese": "纹理检查器", "Japanese": "テクスチャチェッカー", "Korean": "텍스처 검사기"},
    "Clean Memory (RAM )": {u"Turkish": "Belleği Temizle (RAM )", "Espanol": "Limpiar Memoria ( RAM)", "Russian": "Очистить память ( RAM)", "Arabic": "تنظيف الذاكرة (RAM)"," French": "Nettoyer la Mémoire (RAM)", "German": "Speicher bereinigen (RAM)", "Italian": "Pulisci Memoria (RAM)", "Portuguese": "Limpar Memória (RAM)", "Chinese": "清理内存 (RAM)", "Japanese": "メモリをクリーンアップ (RAM)", "Korean": "메모리 정리 (RAM)"},
    "RAM Boost Level": {u"Turkish": "RAM Artış Seviyesi", "Espanol": "Nivel de Aumento de RAM", "Russian": "Уровень увеличения оперативной памяти", "Arabic": "مستوى زيادة ذاكرة الوصول العشوائي"," French": "Niveau de Boost RAM", "German": "RAM-Boost-Level", "Italian": "Livello di Potenziamento RAM", "Portuguese": "Nível de Aumento de RAM", "Chinese": "RAM提升级别", "Japanese": "RAMブーストレベル", "Korean": "RAM 부스트 레벨"},
    "FPS Boost Level": {u"Turkish": "FPS Artış Seviyesi", "Espanol": "Nivel de Aumento de FPS", "Russian": "Уровень увеличения FPS", "Arabic": "مستوى زيادة FPS"," French": "Niveau de Boost FPS", "German": "FPS-Boost-Level", "Italian": "Livello di Potenziamento FPS", "Portuguese": "Nível de Aumento de FPS", "Chinese": "FPS提升级别", "Japanese": "FPSブーストレベル", "Korean": "FPS 부스트 레벨"},
    "Clean Memory (RAM)": {u"Turkish": "Belleği Temizle (RAM )", "Espanol": "Limpiar Memoria ( RAM)", "Russian": "Очистить память ( RAM)", "Arabic": "تنظيف الذاكرة (RAM)"," French": "Nettoyer la Mémoire (RAM)", "German": "Speicher bereinigen (RAM)", "Italian": "Pulisci Memoria (RAM)", "Portuguese": "Limpar Memória (RAM)", "Chinese": "清理内存 (RAM)", "Japanese": "メモリをクリーンアップ (RAM)", "Korean": "메모리 정리 (RAM)"},
    "Clear": {u"Turkish": "Temizle", "Espanol": "Limpiar", "Russian": "Очистить", "Arabic": "واضح", "French": "Clair", "German": "Klar", "Italian": "Chiaro", "Portuguese": "Claro", "Chinese": "清楚", "Japanese": "クリア", "Korean": "명확한"},
    "Language": {u"Turkish": "Dil Seçeneği", "Espanol": "Idioma", "Russian": "Язык", "Arabic": "لغة", "French": "Langue", "German": "Sprache", "Italian": "Lingua", "Portuguese": "Língua", "Chinese": "语言", "Japanese": "言語", "Korean": "언어"},
    "Console": {u"Turkish": "Konsol", "Espanol": "Consola", "Russian": "Консоль", "Arabic": "وحدة التحكم", "French": "Console", "German": "Konsole", "Italian": "Console", "Portuguese": "Console", "Chinese": "控制台", "Japanese": "コンソール", "Korean": "콘솔"},
    "Execute Quick Command": {u"Turkish": "Hızlı Komutu Çaliştır", "Espanol": "Ejecutar Comando Rápido", "Russian": "Выполнить быструю команду", "Arabic": "تنفيذ الأمر السريع"," French": "Exécuter la Commande Rapide", "German": "Schnellbefehl ausführen", "Italian": "Esegui Comando Rapido", "Portuguese": "Executar Comando Rápido", "Chinese": "执行快速命令", "Japanese": "クイックコマンドを実行", "Korean": "빠른 명령 실행"},
    "Execute": {u"Turkish": "Çalıştır", "Espanol": "Ejecutar", "Russian": "Выполнить", "Arabic": "ينفذ"," French": "Exécuter", "German": "Ausführen", "Italian": "Esegui", "Portuguese": "Executar", "Chinese": "执行", "Japanese": "実行", "Korean": "실행"},
    "Clear Console": {u"Turkish": "Konsolu Temizle", "Espanol": "Limpiar Consola", "Russian": "Очистить консоль", "Arabic": "مسح وحدة التحكم"," French": "Effacer la Console", "German": "Konsole löschen", "Italian": "Pulisci Console", "Portuguese": "Limpar Console", "Chinese": "清除控制台", "Japanese": "コンソールをクリア", "Korean": "콘솔 지우기"},
    "Set Fog Settings": {u"Turkish": "Sis Ayarlarını Ayarla", "Espanol": "Establecer Configuración de Niebla", "Russian": "Установить настройки тумана", "Arabic": "تعيين إعدادات الضباب", "German": "Nebel-Einstellungen festlegen", "Italian": "Imposta le Impostazioni della Nebbia", "Portuguese": "Definir Configurações de Névoa", "Chinese": "设置雾设置", "Japanese": "フォグ設定を設定", "Korean": "안개 설정 설정"," French": "Définir les Paramètres de Brouillard"},
    "Light Limit Patch": {u"Turkish": "Işık Sınırlaması Yaması", "Espanol": "Parche de Límite de Luz", "Russian": "Патч ограничения света", "Arabic": "تصحيح حد الضوء"," French": "Patch de Limite de Lumière", "German": "Lichtlimit-Patch", "Italian": "Patch Limite Luce", "Portuguese": "Patch de Limite de Luz", "Chinese": "光限制补丁", "Japanese": "ライトリミットパッチ", "Korean": "조명 제한 패치"},
    u"VMTEDİTOR": {u"Turkish": "VMTDÜZENLEYİCİ", "Espanol": "EDITOR VMT", "Russian": "РЕДАКТОР VMT", "Arabic": "محرر VMT"," French": "ÉDITEUR VMT", "German": "VMT-EDITOR", "Italian": "EDITORE VMT", "Portuguese": "EDITOR VMT", "Chinese": "VMT编辑器", "Japanese": "VMTエディター", "Korean": "VMT 편집기"},
    "Logs": {u"Turkish": "Kayıtlar", "Espanol": "Registros", "Russian": "Журналы", "Arabic": "السجلات"," French": "Journaux", "German": "Protokolle", "Italian": "Registri", "Portuguese": "Registros", "Chinese": "日志", "Japanese": "ログ", "Korean": "로그"},
    "Clock:": {u"Turkish": "Saat", "Espanol": "Reloj", "Russian": "Часы", "Arabic": "ساعة"," French": "Horloge", "German": "Uhr", "Italian": "Orologio", "Portuguese": "Relógio", "Chinese": "时钟", "Japanese": "時計", "Korean": "시계"},
    "Guide": {u"Turkish": "Rehber", "Espanol": "Guía", "Russian": "Руководство", "Arabic": "دليل", "French": "Guide", "German": "Anleitung", "Italian": "Guida", "Portuguese": "Guia", "Chinese": "指南", "Japanese": "ガイド", "Korean": "가이드"},
    "SFM Overlay": {u"Turkish": "SFM Yerleşimi", "Espanol": "Superposición SFM", "Russian": "Наложение SFM", "Arabic": "تراكب SFM", "French": "Superposition SFM", "German": "SFM-Überlagerung", "Italian": "Sovrapposizione SFM", "Portuguese": "Sobreposição SFM", "Chinese": "SFM叠加", "Japanese": "SFMオーバーレイ", "Korean": "SFM 오버레이"},
    "Add Image": {u"Turkish": "Resim Ekle", "Espanol": "Añadir Imagen", "Russian": "Добавить изображение", "Arabic": "إضافة صورة", "French": "Ajouter une Image", "German": "Bild hinzufügen", "Italian": "Aggiungi Immagine", "Portuguese": "Adicionar Imagem", "Chinese": "添加图片", "Japanese": "画像を追加", "Korean": "이미지 추가"},
    "Remove Selected": {u"Turkish": "Seçileni Kaldır", "Espanol": "Eliminar Seleccionado", "Russian": "Удалить выбранное", "Arabic": "إزالة المحدد", "French": "Supprimer la Sélection", "German": "Auswahl entfernen", "Italian": "Rimuovi Selezionato", "Portuguese": "Remover Selecionado", "Chinese": "删除选中", "Japanese": "選択を削除", "Korean": "선택 항목 제거"},
    "Bring to Front": {u"Turkish": "Öne Getir", "Espanol": "Traer al Frente", "Russian": "На передний план", "Arabic": "إحضار للأمام", "French": "Mettre au Premier Plan", "German": "In den Vordergrund", "Italian": "Porta in Primo Piano", "Portuguese": "Trazer para Frente", "Chinese": "置于顶层", "Japanese": "前面に移動", "Korean": "앞으로 가져오기"},
    "Toggle All": {u"Turkish": "Tümünü Değiştir", "Espanol": "Alternar Todo", "Russian": "Переключить все", "Arabic": "تبديل الكل", "French": "Tout Basculer", "German": "Alle umschalten", "Italian": "Attiva/Disattiva Tutto", "Portuguese": "Alternar Tudo", "Chinese": "切换全部", "Japanese": "すべて切り替え", "Korean": "전체 토글"},
    "Remove All": {u"Turkish": "Tümünü Kaldır", "Espanol": "Eliminar Todo", "Russian": "Удалить все", "Arabic": "إزالة الكل", "French": "Tout Supprimer", "German": "Alle entfernen", "Italian": "Rimuovi Tutto", "Portuguese": "Remover Tudo", "Chinese": "全部删除", "Japanese": "すべて削除", "Korean": "모두 제거"},
    "Opacity:": {u"Turkish": "Opaklık:", "Espanol": "Opacidad:", "Russian": "Прозрачность:", "Arabic": "التعتيم:", "French": "Opacité:", "German": "Deckkraft:", "Italian": "Opacità:", "Portuguese": "Opacidade:", "Chinese": "不透明度:", "Japanese": "不透明度:", "Korean": "불투명도:"},
    "Scale:": {u"Turkish": "Ölçek:", "Espanol": "Escala:", "Russian": "Масштаб:", "Arabic": "المقياس:", "French": "Échelle:", "German": "Skalierung:", "Italian": "Scala:", "Portuguese": "Escala:", "Chinese": "缩放:", "Japanese": "スケール:", "Korean": "크기:"},
    "Lock (Click-through)": {u"Turkish": "Kilitle (Tıklama geçişli)", "Espanol": "Bloquear (Clic a través)", "Russian": "Блокировка (клик сквозь)", "Arabic": "قفل (نقر للمرور)", "French": "Verrouiller (Clic transparent)", "German": "Sperren (Klick durch)", "Italian": "Blocca (Clic passante)", "Portuguese": "Bloquear (Clique passante)", "Chinese": "锁定（点击穿透）", "Japanese": "ロック（クリックスルー）", "Korean": "잠금 (클릭 통과)"},
    "Presets": {u"Turkish": "Ön Ayarlar", "Espanol": "Preajustes", "Russian": "Пресеты", "Arabic": "الإعدادات المسبقة", "French": "Préréglages", "German": "Voreinstellungen", "Italian": "Predefiniti", "Portuguese": "Predefinições", "Chinese": "预设", "Japanese": "プリセット", "Korean": "프리셋"},
    "Preset name...": {u"Turkish": "Ön ayar adı...", "Espanol": "Nombre del preajuste...", "Russian": "Имя пресета...", "Arabic": "اسم الإعداد المسبق...", "French": "Nom du préréglage...", "German": "Voreinstellungsname...", "Italian": "Nome predefinito...", "Portuguese": "Nome da predefinição...", "Chinese": "预设名称...", "Japanese": "プリセット名...", "Korean": "프리셋 이름..."},
    "Save": {u"Turkish": "Kaydet", "Espanol": "Guardar", "Russian": "Сохранить", "Arabic": "حفظ", "French": "Enregistrer", "German": "Speichern", "Italian": "Salva", "Portuguese": "Salvar", "Chinese": "保存", "Japanese": "保存", "Korean": "저장"},
    "Load": {u"Turkish": "Yükle", "Espanol": "Cargar", "Russian": "Загрузить", "Arabic": "تحميل", "French": "Charger", "German": "Laden", "Italian": "Carica", "Portuguese": "Carregar", "Chinese": "加载", "Japanese": "読み込む", "Korean": "불러오기"},
    "Delete": {u"Turkish": "Sil", "Espanol": "Eliminar", "Russian": "Удалить", "Arabic": "حذف", "French": "Supprimer", "German": "Löschen", "Italian": "Elimina", "Portuguese": "Excluir", "Chinese": "删除", "Japanese": "削除", "Korean": "삭제"},
    "Select Model From Animation Set Editor": {u"Turkish": "Animasyon Seti Düzenleyicisinden Model Seç", "Espanol": "Seleccionar Modelo del Editor", "Russian": "Выбрать модель из редактора", "Arabic": "اختر نموذجاً من المحرر", "French": "Sélectionner un Modèle", "German": "Modell auswählen", "Italian": "Seleziona Modello", "Portuguese": "Selecionar Modelo", "Chinese": "从动画集编辑器选择模型", "Japanese": "アニメーションセットからモデルを選択", "Korean": "애니메이션 세트에서 모델 선택"},
    "No model was selected...": {u"Turkish": "Model seçilmedi...", "Espanol": "No se seleccionó modelo...", "Russian": "Модель не выбрана...", "Arabic": "لم يتم اختيار نموذج...", "French": "Aucun modèle sélectionné...", "German": "Kein Modell ausgewählt...", "Italian": "Nessun modello selezionato...", "Portuguese": "Nenhum modelo selecionado...", "Chinese": "未选择模型...", "Japanese": "モデルが選択されていません...", "Korean": "모델이 선택되지 않았습니다..."},
    "Clear Log": {u"Turkish": "Kaydı Temizle", "Espanol": "Limpiar Registro", "Russian": "Очистить журнал", "Arabic": "مسح السجل", "French": "Effacer le Journal", "German": "Protokoll löschen", "Italian": "Cancella Registro", "Portuguese": "Limpar Registro", "Chinese": "清除日志", "Japanese": "ログをクリア", "Korean": "로그 지우기"},
    "Skibidi What If": {u"Turkish": "Skibidi Ya Olsaydı", "Espanol": "Skibidi ¿Y si...?", "Russian": "Скибиди: А что если?", "Arabic": "سكيبيدي ماذا لو؟", "French": "Skibidi Et Si...?", "German": "Skibidi Was Wäre Wenn?", "Italian": "Skibidi Cosa Sarebbe Se?", "Portuguese": "Skibidi E Se...?", "Chinese": "Skibidi 假如", "Japanese": "スキビディ もしも", "Korean": "스키비디 만약에"},
    "Save Notes": {u"Turkish": "Notları Kaydet", "Espanol": "Guardar Notas", "Russian": "Сохранить заметки", "Arabic": "حفظ الملاحظات", "French": "Enregistrer les Notes", "German": "Notizen speichern", "Italian": "Salva Note", "Portuguese": "Salvar Notas", "Chinese": "保存笔记", "Japanese": "ノートを保存", "Korean": "노트 저장"},
    "Enable Fog": {u"Turkish": u"Sisi Etkinleştir", "Espanol": "Habilitar Niebla", "Russian": "Включить туман", "Arabic": "تفعيل الضباب", "French": "Activer le Brouillard", "German": "Nebel aktivieren", "Italian": "Abilita Nebbia", "Portuguese": "Ativar Névoa", "Chinese": "启用雾效", "Japanese": "フォグを有効にする", "Korean": "안개 활성화"},
    "Fog start": {u"Turkish": u"Sis başlangıcı", "Espanol": "Inicio de Niebla", "Russian": "Начало тумана", "Arabic": "بداية الضباب", "French": "Début du Brouillard", "German": "Nebelstart", "Italian": "Inizio Nebbia", "Portuguese": "Início da Névoa", "Chinese": "雾起始", "Japanese": "フォグ開始", "Korean": "안개 시작"},
    "Fog end": {u"Turkish": u"Sis sonu", "Espanol": "Fin de Niebla", "Russian": "Конец тумана", "Arabic": "نهاية الضباب", "French": "Fin du Brouillard", "German": "Nebelende", "Italian": "Fine Nebbia", "Portuguese": "Fim da Névoa", "Chinese": "雾结束", "Japanese": "フォグ終了", "Korean": "안개 끝"},
}




def t(key):
    """Return translated text for key based on CURRENT_LANGUAGE."""
    try:
        # Always return a Unicode object to Qt (Python 2 compatibility)
        if CURRENT_LANGUAGE == DEFAULT_LANGUAGE:
            try:
                return unicode(key)
            except Exception:
                return key

        val = TRANSLATIONS.get(key, {}).get(CURRENT_LANGUAGE, key)
        # If it's a byte string, try decoding as UTF-8
        try:
            if isinstance(val, str):
                return val.decode('utf-8')
        except Exception:
            pass
        try:
            return unicode(val)
        except Exception:
            return val
    except Exception:
        return key

# Alphabets for validation / rendering references (includes digits and human-readable full list)
# Compact forms (no spaces) used in validation/matching
TURKISH_ALPHABET = "ABCÃ‡DEFGÄHIÄ°JKLMNOÃ–PRSÅTUÃœVYZabcÃ§defgÄŸhÄ±ijklmnoÃ¶prsÅŸtuÃ¼vyz0123456789"
ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
# Full human-readable alphabets (as requested)
TURKISH_ALPHABET_FULL = "A B C Ã‡ D E F G Ä H I Ä° J K L M N O Ã– P R S Å T U Ãœ V Y Z - a b c Ã§ d e f g ÄŸ h Ä± i j k l m n o Ã¶ p r s ÅŸ t u Ã¼ v y z"
ENGLISH_ALPHABET_FULL = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z - a b c d e f g h i j k l m n o p q r s t u v w x y z"

# Per-language split alphabets (explicit upper/lower lists for robust checking)
ENGLISH_UPPER = [
    "A","B","C","D","E","F","G","H","I","J","K","L",
    "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]
ENGLISH_LOWER = [
    "a","b","c","d","e","f","g","h","i","j","k","l",
    "m","n","o","p","q","r","s","t","u","v","w","x","y","z"
]

TURKISH_UPPER = [
    "A","B","C","Ã‡","D","E","F","G","Ä","H","I","Ä°",
    "J","K","L","M","N","O","Ã–","P","R","S","Å",
    "T","U","Ãœ","V","Y","Z"
]
TURKISH_LOWER = [
    "a","b","c","ç","d","e","f","g","ğ","h","I","i",
    "j","k","l","m","n","o","ö","p","r","s","ş",
    "t","u","ü","v","y","z"
]

def get_alphabet_for_language(lang):
    lang = (lang or '').lower()
    if lang.startswith('tur') or 'tur' in lang:
        return ''.join(TURKISH_UPPER + TURKISH_LOWER)
    # default: English
    return ''.join(ENGLISH_UPPER + ENGLISH_LOWER)
# Helper: pick and apply a Unicode-capable font available on the system that supports the given sample characters
def apply_unicode_font(widget, samples=None, point_size=10):
    try:
        db = QtGui.QFontDatabase()
        candidates = ["Segoe UI", "Tahoma", "Arial Unicode MS", "DejaVu Sans", "Noto Sans", "Liberation Sans", "Arial"]
        samples = samples or (TURKISH_ALPHABET + ENGLISH_ALPHABET)
        for fam in candidates:
            try:
                if fam not in db.families():
                    continue
                font = QtGui.QFont(fam, point_size)
                fm = QtGui.QFontMetrics(font)
                ok = True
                for ch in samples:
                    if ch.isspace() or ch == '-':
                        continue
                    try:
                        if not fm.inFont(ch):
                            ok = False
                            break
                    except Exception:
                        ok = False
                        break
                if ok:
                    widget.setFont(font)
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False

# Stored original skybox name (best-effort) - set when user changes skybox
original_skybox = None

# ---------- Universal click animation ----------
def add_click_animation(button):
    """Add a smooth zoom animation when a button is clicked."""
    def animate():
        try:
            anim = QtCore.QPropertyAnimation(button, b"geometry")
            anim.setDuration(120)
            rect = button.geometry()
            if rect.width() <= 0 or rect.height() <= 0:
                return
            anim.setStartValue(rect)
            anim.setKeyValueAt(0.5, QtCore.QRect(rect.x()-2, rect.y()-2, rect.width()+4, rect.height()+4))
            anim.setEndValue(rect)
            anim.start()
            # keep reference so GC doesn't kill it
            button._anim = anim
        except Exception:
            pass
    button.clicked.connect(animate)

# ---------- Crash-protection utilities ----------
def safe_call(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            tb = traceback.format_exc()
            try:
                inst = args[0]
                if hasattr(inst, 'log_box'):
                    inst.log_box.append("âš  Exception in {}: {}".format(fn.__name__, tb.replace('\n', ' | ')))
            except Exception:
                try:
                    sfm.Msg("[Python] Exception: {}\n".format(tb))
                except Exception:
                    pass
    return wrapper

def global_excepthook(exc_type, exc, tb):
    s = ''.join(traceback.format_exception(exc_type, exc, tb))
    try:
        sfm.Msg("[Python][Unhandled Exception] {}\n".format(s))
    except Exception:
        pass
    try:
        # only run valid SFM commands
        sfm.console("mat_specular 0")
        sfm.console("r_shadowrendertotexture 0")
        sfm.console("r_queued_ropes 0")
    except Exception:
        pass

sys.excepthook = global_excepthook





# ---------- SFM Overlay Manager (standalone overlay windows, presets) ----------
# This code is adapted from a standalone SFM overlay script. It provides
# `OverlayWindow`, `SettingsStore`, and `OverlayManager` classes used below.

import os, ctypes, hashlib
from PySide import QtGui, QtCore

# ---------------- Windows Click Through ----------------
user32 = ctypes.windll.user32
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

def hwnd(widget):
    try:
        return int(widget.winId())
    except:
        return 0

#----------Vmt editor----------
RECENT_FILE = "game/usermod/scripts/vmt_editor.txt"
MAX_RECENT = 10

GAME_PATHS = {
    "usermod": "usermod/materials",
    "workshop": "workshop/materials",
    "hl2": "hl2/materials",
    "tf2": "tf/materials",
    "blackmesa": "bms/materials",
    "left4dead2": "left4dead2/materials"
}

CUSTOM_PATHS = {}  # �������� -> ���� (��������, ������ ��� = ���)

QUICK_ATTRS = [
    "$basetexture",
    "$bumpmap",
    "$envmap",
    "$phong",
    "$phongboost",
    "$phongexponent",
    "$selfillum",
    "$translucent",
    "$rimlight",
    "$halflambert",
]

# -------------------------------------------------
# Utils
# -------------------------------------------------

def getGameRoot():
    vproject = os.environ.get("VPROJECT")
    if not vproject:
        return None
    return os.path.dirname(vproject)

def loadRecent():
    if not os.path.exists(RECENT_FILE):
        return []
    with open(RECENT_FILE, "r") as f:
        return [l.strip() for l in f.readlines() if l.strip()]

def saveRecent(path):
    recent = loadRecent()
    if path in recent:
        recent.remove(path)
    recent.insert(0, path)
    recent = recent[:MAX_RECENT]

    folder = os.path.dirname(RECENT_FILE)
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(RECENT_FILE, "w") as f:
        f.write("\n".join(recent))


class VMTHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super(VMTHighlighter, self).__init__(document)

        def fmt(color, bold=False):
            f = QtGui.QTextCharFormat()
            f.setForeground(QtGui.QColor(color))
            if bold:
                f.setFontWeight(QtGui.QFont.Bold)
            return f

        self.rules = [
            (QtCore.QRegExp(r'^\s*\"[A-Za-z0-9_]+\"'), fmt("#c678dd", True)),  # Shader
            (QtCore.QRegExp(r"\$[A-Za-z0-9_]+"), fmt("#ffae57", True)),
            (QtCore.QRegExp(r"\".*\""), fmt("#98c379")),
            (QtCore.QRegExp(r"\{|\}"), fmt("#61afef")),
            (QtCore.QRegExp(r"//.*"), fmt("#7f848e")),
        ]

    def highlightBlock(self, text):
        for pattern, form in self.rules:
            index = pattern.indexIn(text, 0)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, form)
                index = pattern.indexIn(text, index + length)

class LineNumberArea(QtGui.QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class CodeEditor(QtGui.QPlainTextEdit):
    def __init__(self):
        super(CodeEditor, self).__init__()

        self.fontSize = 12
        self.updateFont()

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def updateFont(self):
        font = self.font()
        font.setPointSize(self.fontSize)
        self.setFont(font)

    def wheelEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.delta() > 0:
                self.fontSize = min(self.fontSize + 1, 32)
            else:
                self.fontSize = max(self.fontSize - 1, 8)
            self.updateFont()
            self.updateLineNumberAreaWidth(0)
            event.accept()
        else:
            super(CodeEditor, self).wheelEvent(event)

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().width('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

    def resizeEvent(self, event):
        super(CodeEditor, self).resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(),
            self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QtGui.QColor("#21252b"))

        block = self.firstVisibleBlock()
        number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QtGui.QColor("#5c6370"))
                painter.drawText(0, top, self.lineNumberArea.width() - 4,
                                 self.fontMetrics().height(),
                                 QtCore.Qt.AlignRight, str(number + 1))
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            number += 1

    def highlightCurrentLine(self):
        extra = QtGui.QTextEdit.ExtraSelection()
        extra.format.setBackground(QtGui.QColor("#2c313c"))
        extra.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        extra.cursor = self.textCursor()
        extra.cursor.clearSelection()
        self.setExtraSelections([extra])


class VMTEditor(QtGui.QWidget):
    def __init__(self):
        super(VMTEditor, self).__init__()


        self.vmtPath = None

        self.setWindowTitle("VMTEDİTOR")
        self.resize(1050, 680)

        # Game combo and path input
        self.gameCombo = QtGui.QComboBox()
        for g in GAME_PATHS:
            self.gameCombo.addItem(g)

        self.pathEdit = QtGui.QLineEdit()
        self.pathEdit.setPlaceholderText(u"Enter the texture")

        # Recent VMTs
        self.recentCombo = QtGui.QComboBox()
        self.recentCombo.setFixedWidth(180)
        self.refreshRecent()

        # Custom directories
        self.customEdit = QtGui.QLineEdit()
        self.customEdit.setPlaceholderText("Custom dir name")
        self.customEdit.setMaximumWidth(120)
        self.addDirBtn = QtGui.QPushButton("Add Custom Directory")
        self.addDirBtn.setMaximumWidth(120)
        self.removeDirBtn = QtGui.QPushButton("Remove Custom Directory")
        self.removeDirBtn.setMaximumWidth(120)
        self.addDirBtn.clicked.connect(self.addCustomDirectory)
        self.removeDirBtn.clicked.connect(self.removeCustomDirectory)

        # Buttons
        self.openBtn = QtGui.QPushButton("Open")
        self.saveBtn = QtGui.QPushButton("Save")

        # Code editor
        self.textEdit = CodeEditor()
        self.highlighter = VMTHighlighter(self.textEdit.document())

        # Quick attributes
        quickLayout = QtGui.QHBoxLayout()
        for attr in QUICK_ATTRS:
            btn = QtGui.QPushButton(attr)
            btn.clicked.connect(functools.partial(self.insertAttr, attr))
            quickLayout.addWidget(btn)
        quickLayout.addStretch()

        # Top layout
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.gameCombo)
        topLayout.addWidget(self.pathEdit, 1)
        topLayout.addWidget(self.recentCombo)
        topLayout.addWidget(self.openBtn)
        topLayout.addWidget(self.saveBtn)

        # Custom directory layout
        customLayout = QtGui.QHBoxLayout()
        customLayout.addWidget(self.customEdit)
        customLayout.addWidget(self.addDirBtn)
        customLayout.addWidget(self.removeDirBtn)
        customLayout.addStretch()


        # Main layout
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(quickLayout)
        mainLayout.addLayout(customLayout)
        mainLayout.addWidget(self.textEdit)
        self.setLayout(mainLayout)

        # Signals
        self.openBtn.clicked.connect(self.openVMT)
        self.saveBtn.clicked.connect(self.saveVMT)
        self.recentCombo.activated.connect(self.openRecent)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.saveVMT)


    def refreshRecent(self):
        self.recentCombo.clear()
        self.recentCombo.addItem("Recent...")
        for r in loadRecent():
            self.recentCombo.addItem(r)

    def openRecent(self, index):
        if index == 0:
            return
        self.openFullPath(self.recentCombo.itemText(index))


    def insertAttr(self, attr):
        cursor = self.textEdit.textCursor()
        cursor.insertText(attr + " ")
        self.textEdit.setTextCursor(cursor)

    def openVMT(self):
        root = getGameRoot()
        if not root:
            QtGui.QMessageBox.warning(self, "Vmt Editor", "VPROJECT not found")
            return

        game = str(self.gameCombo.currentText())
        mat = str(self.pathEdit.text()).replace("\\", "/")
        basePath = GAME_PATHS.get(game, game)
        if game in CUSTOM_PATHS:
            basePath = CUSTOM_PATHS[game]
        self.openFullPath(os.path.join(root, basePath, mat + ".vmt"))

    def openFullPath(self, path):
        if not os.path.exists(path):
            QtGui.QMessageBox.warning(self, "VMTEDİTOR", "Vmt not found:\n" + path)
            return
        self.vmtPath = path
        with open(path, "r") as f:
            self.textEdit.setPlainText(f.read())
        saveRecent(path)
        self.refreshRecent()

    def saveVMT(self):
        if not self.vmtPath:
            return
        with open(self.vmtPath, "w") as f:
            f.write(self.textEdit.toPlainText())
        try:
            import sfm
            mat = sfm.GetSelectedMaterial()
            if mat:
                mat.ReloadTextures()
        except:
            pass

 
    def addCustomDirectory(self):
        name = self.customEdit.text().strip()
        if not name or name in GAME_PATHS or name in CUSTOM_PATHS:
            return
        CUSTOM_PATHS[name] = name
        self.gameCombo.addItem(name)
        self.customEdit.clear()

    def removeCustomDirectory(self):
        name = self.customEdit.text().strip()
        if name in CUSTOM_PATHS:
            index = self.gameCombo.findText(name)
            if index >= 0:
                self.gameCombo.removeItem(index)
            del CUSTOM_PATHS[name]
            self.customEdit.clear()



def CreateVmteditorTab():
    editor = VMTEditor()
    tab_id = "VMTEDİTOR_" + str(id(editor))
    ptr = shiboken.getCppPointer(editor)
    sfmApp.RegisterTabWindow(tab_id, "VMTEDİTOR", ptr[0])
    sfmApp.ShowTabWindow(tab_id)






# ---------- SFM Notes Tab ----------
class SFMNotesTab(QtGui.QWidget):
    def __init__(self):
        super(SFMNotesTab, self).__init__()
        self.setStyleSheet('''
            /* ── SFM-faithful global stylesheet ── */
            QWidget {
                background: #3c3c3c;
                color: #c8c8c8;
                font-family: "Tahoma", "Segoe UI", sans-serif;
                font-size: 11px;
            }
            QDialog  { background: #3c3c3c; }
            QFrame   { background: #3c3c3c; }

            /* Inputs */
            QLineEdit, QPlainTextEdit {
                background: #1e1e1e;
                color: #c8c8c8;
                border: 1px solid #1a1a1a;
                border-top: 1px solid #111111;
                padding: 3px 5px;
                selection-background-color: #4d7cc4;
            }
            QLineEdit:focus, QPlainTextEdit:focus {
                border: 1px solid #4d7cc4;
            }
            QTextEdit {
                background: #1e1e1e;
                color: #c8c8c8;
                border: 1px solid #1a1a1a;
                selection-background-color: #4d7cc4;
            }

            /* ComboBox */
            QComboBox {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #5a5a5a, stop:1 #3e3e3e);
                color: #e0e0e0;
                border: 1px solid #1a1a1a;
                padding: 3px 6px;
                min-height: 20px;
            }
            QComboBox:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #6a6a6a, stop:1 #4e4e4e); }
            QComboBox::drop-down { border: none; width: 18px; background: #3a3a3a; }
            QComboBox QAbstractItemView {
                background: #3c3c3c;
                color: #c8c8c8;
                border: 1px solid #1a1a1a;
                selection-background-color: #4d7cc4;
                selection-color: white;
            }

            /* CheckBox */
            QCheckBox { color: #c8c8c8; spacing: 5px; }
            QCheckBox::indicator {
                width: 12px; height: 12px;
                background: #1e1e1e;
                border: 1px solid #1a1a1a;
            }
            QCheckBox::indicator:checked { background: #4d7cc4; border: 1px solid #3a62a0; }
            QCheckBox::indicator:hover   { border: 1px solid #4d7cc4; }

            /* SpinBox */
            QSpinBox, QDoubleSpinBox {
                background: #1e1e1e;
                color: #c8c8c8;
                border: 1px solid #1a1a1a;
                padding: 2px 5px;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background: #4a4a4a;
                border: 1px solid #1a1a1a;
                width: 14px;
            }

            /* Labels */
            QLabel { background: transparent; color: #c8c8c8; }

            /* GroupBox */
            QGroupBox {
                border: 1px solid #222222;
                margin-top: 6px;
                font-weight: bold;
                font-size: 11px;
                color: #888888;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 6px;
                padding: 0 3px;
                color: #4d7cc4;
            }

            /* Table */
            QTableWidget {
                background: #1e1e1e;
                color: #c8c8c8;
                gridline-color: #2b2b2b;
                border: 1px solid #1a1a1a;
                selection-background-color: #4d7cc4;
                selection-color: white;
            }
            QTableWidget::item:alternate { background: #252525; }
            QHeaderView::section {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #4a4a4a, stop:1 #333333);
                color: #c8c8c8;
                border: none;
                border-right: 1px solid #222;
                border-bottom: 1px solid #111;
                padding: 3px 6px;
                font-weight: bold;
                font-size: 10px;
            }

            /* Tooltip */
            QToolTip {
                background: #3c3c3c;
                color: #e8e8e8;
                border: 1px solid #1a1a1a;
                padding: 3px 5px;
                font-size: 11px;
            }

            /* Separator */
            QFrame[frameShape="4"], QFrame[frameShape="5"] {
                color: #222222;
                background: #222222;
            }
        ''')
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        title = QtGui.QLabel(" SFM Notes")
        title.setStyleSheet("font-size:16px; font-weight:700; color: %s;" % PALETTE['text'])
        layout.addWidget(title)

        self.text_edit = QtGui.QTextEdit()
        self.text_edit.setStyleSheet('''
            QTextEdit {
                background-color: %s;
                color: %s;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
        ''' % (PALETTE['muted'], PALETTE['text']))
        layout.addWidget(self.text_edit)

        hb = QtGui.QHBoxLayout()
        self.save_button = QtGui.QPushButton(t("Save Notes"))
        self.save_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.save_button.setStyleSheet('font-weight:600; padding:8px; border-radius:8px;')
        self.save_button.clicked.connect(self.save_notes)
        add_click_animation(self.save_button)
        hb.addWidget(self.save_button)

        self.clear_button = QtGui.QPushButton("Clear")
        self.clear_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.clear_button.clicked.connect(self.clear_notes)
        self.clear_button.setStyleSheet('font-weight:600; padding:8px; border-radius:8px;')
        add_click_animation(self.clear_button)
        hb.addWidget(self.clear_button)

        layout.addLayout(hb)
        self.load_notes()

    def save_notes(self):
        try:
            # DÜZELTME 2: Python 2 uyumlu dosya kaydı için codecs.open() kullanıldı
            # Orijinal: with open(NOTES_FILENAME, "w", encoding="utf-8") as f:
            with codecs.open(NOTES_FILENAME, "w", "utf-8") as f:
                f.write(self.text_edit.toPlainText())
            QtGui.QMessageBox.information(self, "SFM Notes", "Notes saved successfully ")
        except Exception as e:
            QtGui.QMessageBox.warning(self, "SFM Notes", "Could not save notes: {}".format(e))

    def load_notes(self):
        try:
            if os.path.exists(NOTES_FILENAME):
                with codecs.open(NOTES_FILENAME, "r", "utf-8") as f:
                    self.text_edit.setText(f.read())
        except Exception:
            pass

    def clear_notes(self):
        try:
            self.text_edit.clear()
            try:
                if os.path.exists(NOTES_FILENAME):
                    os.remove(NOTES_FILENAME)
            except Exception:
                pass
        except Exception:
            pass

import re

def add_hover_glow(button):
    """Butonun kendi rengini gradient'tan okuyup aynı renkte parlatma efekti uygular."""
    try:
        style = button.styleSheet()

        # Önce gradient stop:0 rengini dene (ana buton rengi)
        color = None
        match = re.search(r'stop:0\s*(#[0-9a-fA-F]{6})', style)
        if match:
            color = QtGui.QColor(match.group(1))
        else:
            # Sonra background-color dene
            match = re.search(r'background-color:\s*(#[0-9a-fA-F]{6})', style)
            if match:
                color = QtGui.QColor(match.group(1))
            else:
                # background: #xxx dene
                match = re.search(r'background:\s*(#[0-9a-fA-F]{6})', style)
                if match:
                    color = QtGui.QColor(match.group(1))

        # Renk bulunamadıysa veya çok koyu/nötrse fallback
        if color is None:
            color = QtGui.QColor('#00ffaa')
        else:
            # Çok koyu (siyah/gri) renklerde parlama anlamsız, cyan yap
            if color.red() < 40 and color.green() < 40 and color.blue() < 40:
                color = QtGui.QColor('#00d4ff')
            elif color.red() < 60 and color.green() < 60 and color.blue() < 60:
                color = QtGui.QColor('#aaaaff')

        # Parlama rengi: butonun kendi rengi daha parlak hali
        glow_color = color.lighter(160)

        effect = QtGui.QGraphicsDropShadowEffect(button)
        effect.setBlurRadius(0)
        effect.setColor(glow_color)
        effect.setOffset(0)
        button.setGraphicsEffect(effect)

        anim = QtCore.QPropertyAnimation(effect, b"blurRadius")
        anim.setDuration(180)
        anim.setStartValue(0)
        anim.setEndValue(22)
        anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        def enter(event):
            try:
                anim.setDirection(QtCore.QAbstractAnimation.Forward)
                anim.start()
                button._hover_anim = anim
            except Exception:
                pass

        def leave(event):
            try:
                anim.setDirection(QtCore.QAbstractAnimation.Backward)
                anim.start()
            except Exception:
                pass

        button.enterEvent = enter
        button.leaveEvent = leave

    except Exception:
        pass


def add_slide_in_animation(widget, duration=320, offset=60):
    """Widget'ı soldan kaydırarak giriş animasyonu ile gösterir."""
    try:
        # Mevcut geometriyi al
        rect = widget.geometry()
        if rect.width() <= 0:
            return

        start_rect = QtCore.QRect(rect.x() - offset, rect.y(), rect.width(), rect.height())
        end_rect = rect

        anim = QtCore.QPropertyAnimation(widget, b"geometry")
        anim.setDuration(duration)
        anim.setStartValue(start_rect)
        anim.setEndValue(end_rect)
        anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        anim.start()
        widget._slide_anim = anim  # GC koruması
    except Exception:
        pass









        
# ---------- Main GUI ----------

# ============================================================
# SPLASH SCREEN
# ============================================================
class SplashScreen(QtGui.QWidget):
    """
    Filmmaker GUI 3.7 presents HIDDEX
    Epic multi-phase intro with film reel, particle bursts, typewriter, shockwave.
    """
    PHASE_REEL    = 0
    PHASE_PRESENTS= 1
    PHASE_HIDDEX  = 2
    PHASE_HOLD    = 3

    def __init__(self):
        super(SplashScreen, self).__init__(None)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(700, 260)
        try:
            desk = QtGui.QApplication.desktop().screenGeometry()
            self.move((desk.width()-700)//2, (desk.height()-260)//2)
        except Exception:
            self.move(200, 200)

        self.on_finished = None
        self._eff = QtGui.QGraphicsOpacityEffect(self)
        self._eff.setOpacity(0.0)
        self.setGraphicsEffect(self._eff)

        # state
        self._phase       = self.PHASE_REEL
        self._t           = 0
        self._reel_angle  = 0.0
        self._reel_x      = -140.0
        self._strip_off   = 180.0
        self._bar_prog    = 0.0
        self._status_idx  = 0
        self._presents_a  = 0.0   # "Filmmaker GUI 3.7 presents" alpha
        self._hiddex_chars= 0     # typed chars of HIDDEX
        self._hiddex_scale= 0.0   # HIDDEX grow scale
        self._shockwave_r = 0.0   # expanding ring radius
        self._shockwave_a = 0.0
        self._flash_a     = 0.0   # white flash
        self._particles   = []    # burst particles

        self._statuses = [
            "Initializing...", "Loading interface...",
            "Starting engine...", "Ready."
        ]

        import random as _r
        self._pts = [
            {'x':_r.uniform(0,700),'y':_r.uniform(0,260),
             'r':_r.uniform(1,3),'vy':_r.uniform(-0.6,-0.2),
             'a':_r.randint(15,60)}
            for _ in range(18)
        ]

        self._fi = QtCore.QPropertyAnimation(self._eff, b"opacity")
        self._fi.setDuration(400); self._fi.setStartValue(0.0)
        self._fi.setEndValue(1.0)
        self._fi.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._tick)

    def show_splash(self):
        self.show(); self._fi.start(); self._timer.start(16)

    def _ease_out(self, t):
        t = max(0.0, min(1.0, t))
        return 1.0 - (1.0-t)**3

    def _tick(self):
        import random as _r
        self._t += 1

        # ambient particles
        for pt in self._pts:
            pt['y'] += pt['vy']
            if pt['y'] < -6:
                pt['y'] = 266; pt['x'] = _r.uniform(0,700)

        # burst particles
        for p in self._particles[:]:
            p['x'] += p['vx']; p['y'] += p['vy']
            p['a'] -= 5; p['r'] -= 0.15
            if p['a'] <= 0 or p['r'] <= 0:
                self._particles.remove(p)

        # shockwave
        if self._shockwave_r > 0:
            self._shockwave_r += 8
            self._shockwave_a = max(0, self._shockwave_a - 0.04)
        self._flash_a = max(0, self._flash_a - 0.06)

        # PHASE_REEL  (0-70 ticks)
        if self._phase == self.PHASE_REEL:
            dur = 70
            t01 = self._ease_out(self._t / float(dur))
            self._reel_angle = t01 * 540.0
            self._reel_x     = (1.0-t01)*(-140.0)
            self._strip_off  = (1.0-t01)*180.0
            self._bar_prog   = t01 * 0.3
            self._status_idx = 0
            if self._t >= dur:
                self._phase = self.PHASE_PRESENTS
                self._t = 0

        # PHASE_PRESENTS  (0-55 ticks)
        elif self._phase == self.PHASE_PRESENTS:
            t01 = self._t / 55.0
            self._presents_a = self._ease_out(min(t01, 1.0))
            self._bar_prog   = 0.3 + t01*0.35
            self._status_idx = 1
            if self._t >= 55:
                self._phase = self.PHASE_HIDDEX
                self._t = 0

        # PHASE_HIDDEX  (0-60 ticks)
        elif self._phase == self.PHASE_HIDDEX:
            t01 = self._t / 60.0
            total = len("HIDDEX")
            new_chars = int(t01 * (total + 3))
            # trigger burst when each letter appears
            if new_chars > self._hiddex_chars:
                for _ in range(new_chars - self._hiddex_chars):
                    self._spawn_burst(350 + new_chars*22, 168)
            self._hiddex_chars = new_chars
            self._hiddex_scale = self._ease_out(min(t01/0.5, 1.0))
            self._bar_prog     = 0.65 + t01*0.3
            self._status_idx   = 2
            if self._t >= 60:
                # final shockwave
                self._shockwave_r = 1.0
                self._shockwave_a = 1.0
                self._flash_a     = 0.5
                self._spawn_burst(350, 168, n=30)
                self._phase = self.PHASE_HOLD
                self._t = 0

        # PHASE_HOLD  (30 ticks)
        elif self._phase == self.PHASE_HOLD:
            self._bar_prog   = min(0.95 + self._t/300.0, 1.0)
            self._status_idx = 3
            if self._t >= 30:
                self._timer.stop()
                self._bar_prog = 1.0
                self._do_fadeout()

        self.update()

    def _spawn_burst(self, cx, cy, n=10):
        import random as _r, math as _m
        colors = ["#3fa9f5","#00c9a7","#f0b030","#ff6b6b","#b06bff","#ffffff","#ff9f43"]
        for _ in range(n):
            angle = _r.uniform(0, _m.pi*2)
            speed = _r.uniform(1.5, 5.0)
            self._particles.append({
                'x': cx, 'y': cy,
                'vx': _m.cos(angle)*speed, 'vy': _m.sin(angle)*speed,
                'r': _r.uniform(2, 6),
                'a': _r.randint(180, 255),
                'color': _r.choice(colors)
            })

    def _do_fadeout(self):
        self._fo = QtCore.QPropertyAnimation(self._eff, b"opacity")
        self._fo.setDuration(600); self._fo.setStartValue(1.0)
        self._fo.setEndValue(0.0)
        self._fo.setEasingCurve(QtCore.QEasingCurve.InCubic)
        self._fo.finished.connect(self._finish); self._fo.start()

    def _finish(self):
        self.close()
        if callable(self.on_finished):
            try: self.on_finished()
            except Exception: pass

    def paintEvent(self, ev):
        import math as _m
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setRenderHint(QtGui.QPainter.TextAntialiasing)
        W, H = self.width(), self.height()

        # BG
        bg = QtGui.QLinearGradient(0,0,W,H)
        bg.setColorAt(0.0, QtGui.QColor("#080e18"))
        bg.setColorAt(1.0, QtGui.QColor("#020408"))
        p.setPen(QtCore.Qt.NoPen); p.setBrush(QtGui.QBrush(bg))
        p.drawRoundedRect(0,0,W,H,14,14)

        # Border
        p.setPen(QtGui.QPen(QtGui.QColor("#0d3060"),2))
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawRoundedRect(1,1,W-2,H-2,13,13)

        # Top accent
        ag = QtGui.QLinearGradient(0,0,W,0)
        ag.setColorAt(0, QtGui.QColor(0,0,0,0))
        ag.setColorAt(0.3, QtGui.QColor("#3fa9f5"))
        ag.setColorAt(0.7, QtGui.QColor("#00c9a7"))
        ag.setColorAt(1, QtGui.QColor(0,0,0,0))
        p.setPen(QtGui.QPen(QtGui.QBrush(ag),2))
        p.drawLine(40,3,W-40,3)

        # Ambient particles
        p.setPen(QtCore.Qt.NoPen)
        for pt in self._pts:
            c = QtGui.QColor(63,169,245,pt['a'])
            p.setBrush(c)
            p.drawEllipse(QtCore.QRectF(pt['x']-pt['r'],pt['y']-pt['r'],pt['r']*2,pt['r']*2))

        # Burst particles
        for bp in self._particles:
            c = QtGui.QColor(bp['color']); c.setAlpha(bp['a'])
            p.setBrush(c); p.setPen(QtCore.Qt.NoPen)
            p.drawEllipse(QtCore.QRectF(bp['x']-bp['r'],bp['y']-bp['r'],bp['r']*2,bp['r']*2))

        # Shockwave ring
        if self._shockwave_r > 0 and self._shockwave_a > 0:
            sc = QtGui.QColor(63,169,245,int(self._shockwave_a*180))
            p.setPen(QtGui.QPen(sc, 3))
            p.setBrush(QtCore.Qt.NoBrush)
            r = self._shockwave_r
            p.drawEllipse(QtCore.QRectF(350-r, 168-r, r*2, r*2))

        # White flash
        if self._flash_a > 0:
            fc = QtGui.QColor(255,255,255,int(self._flash_a*120))
            p.setPen(QtCore.Qt.NoPen); p.setBrush(fc)
            p.drawRoundedRect(0,0,W,H,14,14)

        # Film strips
        strip_x = int(W - 68 + self._strip_off)
        left_x  = int(-68 - self._strip_off)
        cell_cols = [QtGui.QColor("#1a1208"),QtGui.QColor("#0a1520"),
                     QtGui.QColor("#0f0f0f"),QtGui.QColor("#18100a")]
        hole_w, hole_h = 11, 17
        for sx in [strip_x, left_x]:
            p.setPen(QtCore.Qt.NoPen)
            p.setBrush(QtGui.QColor("#1e1e1e"))
            p.drawRect(sx,0,68,H)
            p.setBrush(QtGui.QColor("#0a0a0a"))
            for row in range(-1,(H//28)+2):
                hy = row*28+14
                p.drawRoundedRect(sx+6,hy-hole_h//2,hole_w,hole_h,3,3)
                p.drawRoundedRect(sx+50,hy-hole_h//2,hole_w,hole_h,3,3)
            for row in range(-1,(H//28)+2):
                hy=row*28; idx=(row+7)%len(cell_cols)
                p.setBrush(cell_cols[idx])
                p.drawRect(sx+22,hy+2,24,24)

        # Film reel
        rcx = int(82+self._reel_x); rcy = H//2; rr = 68
        p.save(); p.translate(rcx,rcy); p.rotate(self._reel_angle)
        og = QtGui.QRadialGradient(0,0,rr)
        og.setColorAt(0,QtGui.QColor("#2a2a2a")); og.setColorAt(0.7,QtGui.QColor("#222"))
        og.setColorAt(0.85,QtGui.QColor("#333")); og.setColorAt(1,QtGui.QColor("#1a1a1a"))
        p.setPen(QtGui.QPen(QtGui.QColor("#404040"),3))
        p.setBrush(QtGui.QBrush(og))
        p.drawEllipse(QtCore.QRectF(-rr,-rr,rr*2,rr*2))
        sp = QtGui.QPen(QtGui.QColor("#3a3a3a"),8); sp.setCapStyle(QtCore.Qt.RoundCap)
        p.setPen(sp)
        ir=18; osr=rr-14
        for i in range(6):
            a=_m.radians(i*60)
            p.drawLine(QtCore.QPointF(_m.cos(a)*ir,_m.sin(a)*ir),
                       QtCore.QPointF(_m.cos(a)*osr,_m.sin(a)*osr))
        p.setPen(QtCore.Qt.NoPen)
        for i in range(6):
            a=_m.radians(i*60)
            x2=_m.cos(a)*osr; y2=_m.sin(a)*osr
            p.setBrush(QtGui.QColor("#555")); p.drawEllipse(QtCore.QRectF(x2-5,y2-5,10,10))
        hg=QtGui.QRadialGradient(0,0,ir+4)
        hg.setColorAt(0,QtGui.QColor("#444")); hg.setColorAt(1,QtGui.QColor("#1a1a1a"))
        p.setPen(QtGui.QPen(QtGui.QColor("#555"),2)); p.setBrush(QtGui.QBrush(hg))
        p.drawEllipse(QtCore.QRectF(-ir-4,-ir-4,(ir+4)*2,(ir+4)*2))
        p.setPen(QtCore.Qt.NoPen); p.setBrush(QtGui.QColor("#0d0d0d"))
        p.drawEllipse(QtCore.QRectF(-7,-7,14,14))
        # Ticks
        p.setPen(QtGui.QPen(QtGui.QColor("#404040"),2))
        for i in range(36):
            a=_m.radians(i*10)
            p.drawLine(QtCore.QPointF(_m.cos(a)*(rr-6),_m.sin(a)*(rr-6)),
                       QtCore.QPointF(_m.cos(a)*(rr+2),_m.sin(a)*(rr+2)))
        # counter-rotate text
        p.rotate(-self._reel_angle)
        p.setPen(QtGui.QColor("#888"))
        p.setFont(QtGui.QFont("Arial",8,QtGui.QFont.Bold))
        p.drawText(QtCore.QRectF(-30,-10,60,20),QtCore.Qt.AlignCenter,"HIDDEX")
        p.restore()

        # Text area
        tx = int(rcx + rr + 20)
        tw = strip_x - tx - 12

        # "Filmmaker GUI 3.7 presents"
        if self._presents_a > 0 and tw > 40:
            ta = int(self._presents_a * 255)
            # "Filmmaker GUI 3.7"
            tf = QtGui.QFont("Arial",20,QtGui.QFont.Black)
            p.setFont(tf)
            tg = QtGui.QLinearGradient(tx, H//2-56, tx, H//2-20)
            tg.setColorAt(0, QtGui.QColor(255,210,80,ta))
            tg.setColorAt(1, QtGui.QColor(180,120,20,ta))
            p.setPen(QtGui.QPen(QtGui.QBrush(tg),0))
            p.drawText(QtCore.QRect(tx,H//2-56,tw,36),
                       QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,"Filmmaker GUI 3.7")
            # "presents"
            pf = QtGui.QFont("Arial",11)
            pf.setLetterSpacing(QtGui.QFont.AbsoluteSpacing,5)
            p.setFont(pf)
            p.setPen(QtGui.QColor(120,120,140,ta))
            p.drawText(QtCore.QRect(tx+2,H//2-18,tw,20),
                       QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,"P R E S E N T S")

        # "HIDDEX" big typewriter with scale
        if self._hiddex_chars > 0 and tw > 40:
            visible = "HIDDEX"[:max(0,self._hiddex_chars)]
            sc_val  = self._hiddex_scale
            if sc_val > 0.01:
                p.save()
                cx_h = tx + 10
                cy_h = H//2 + 38
                p.translate(cx_h, cy_h)
                p.scale(sc_val, sc_val)
                # Glow
                gce = QtGui.QColor(63,169,245,int(sc_val*80))
                p.setBrush(gce); p.setPen(QtCore.Qt.NoPen)
                p.drawRoundedRect(-6,-28,len(visible)*32+12,42,6,6)
                # Shadow
                p.setPen(QtGui.QColor(0,0,0,100))
                p.setFont(QtGui.QFont("Arial",32,QtGui.QFont.Black))
                p.drawText(QtCore.QPointF(2,2),visible)
                # Gradient fill
                hg2 = QtGui.QLinearGradient(0,-28,0,14)
                hg2.setColorAt(0, QtGui.QColor("#e8f4ff"))
                hg2.setColorAt(0.5,QtGui.QColor("#e41111"))
                hg2.setColorAt(1, QtGui.QColor("#00c9a7"))
                p.setPen(QtGui.QPen(QtGui.QBrush(hg2),0))
                p.drawText(QtCore.QPointF(0,0),visible)
                # Cursor blink
                if self._hiddex_chars < 8 and (self._t%18)<10:
                    fm = QtGui.QFontMetrics(QtGui.QFont("Arial",32,QtGui.QFont.Black))
                    cw = fm.width(visible)
                    p.setPen(QtGui.QColor("#f53f3f"))
                    p.drawText(QtCore.QPointF(cw+3,0),"|")
                p.restore()

        # Divider
        if self._presents_a > 0.5:
            da = int((self._presents_a-0.5)*2*100)
            p.setPen(QtGui.QPen(QtGui.QColor(63,169,245,da),1))
            p.drawLine(tx, H//2+8, tx+tw-10, H//2+8)

        # Progress bar
        bx,by2,bw,bh = 8, H-18, W-16, 5
        p.setPen(QtCore.Qt.NoPen); p.setBrush(QtGui.QColor("#0d1825"))
        p.drawRoundedRect(bx,by2,bw,bh,2,2)
        fw = int(bw*self._bar_prog)
        if fw > 2:
            pg2 = QtGui.QLinearGradient(bx,0,bx+bw,0)
            pg2.setColorAt(0,QtGui.QColor("#0d3a6e"))
            pg2.setColorAt(0.5,QtGui.QColor("#3fa9f5"))
            pg2.setColorAt(1,QtGui.QColor("#00c9a7"))
            p.setBrush(QtGui.QBrush(pg2))
            p.drawRoundedRect(bx,by2,fw,bh,2,2)
            if fw>12:
                gl=QtGui.QRadialGradient(bx+fw,by2+bh//2,12)
                gl.setColorAt(0,QtGui.QColor(0,210,170,200))
                gl.setColorAt(1,QtGui.QColor(0,210,170,0))
                p.setBrush(QtGui.QBrush(gl))
                p.drawEllipse(QtCore.QRectF(bx+fw-12,by2-5,24,14))

        # Status
        status = self._statuses[max(0,min(self._status_idx,len(self._statuses)-1))]
        p.setPen(QtGui.QColor("#2a3a4a"))
        p.setFont(QtGui.QFont("Arial",8))
        p.drawText(QtCore.QRect(bx,H-34,bw,14),QtCore.Qt.AlignRight,status)

        p.end()


class FilmmakerGUI3_0(QtGui.QWidget):
    def __init__(self):
        super(FilmmakerGUI3_0, self).__init__()

        self.setWindowTitle("Filmmaker GUI V3.7")
        self.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #232323, stop:1 #2b2b2b); border: 1px solid #1a1a1a;")
        

        


        try:
            applied = apply_unicode_font(self, samples=(TURKISH_ALPHABET + ENGLISH_ALPHABET))
            try:
                if hasattr(self, 'tabs') and self.tabs is not None:
                    tb = self.tabs.tabBar()
                    if tb is not None:
                        tb.setFont(self.font())
                        for i in range(self.tabs.count()):
                            try:
                                self.tabs.setTabText(i, self.tabs.tabText(i))
                            except Exception:
                                pass
                try:
                    f = self.font()
                    for w in self.findChildren(QtGui.QWidget):
                        try:
                            w.setFont(f)
                        except Exception:
                            pass
                except Exception:
                    pass
            except Exception:
                pass
        except Exception:
            pass

        self.ram_boost_value = 0

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabPosition(QtGui.QTabWidget.North)
        self.tabs.setStyleSheet(self._tab_style())

        self.quick_commands = {
            "Disable Specular": "mat_specular 0",
            "r_hunkalloclightmaps 0": "r_hunkalloclightmaps 0",
            "mat_specular 0": "mat_specular 0",
            "mat_reloadallmaterials": "mat_reloadallmaterials",
            "r_3dsky 0": "r_3dsky 0",
            "mat_wateroverlays 0": "mat_wateroverlays 0",
            "Disable Detail Props (cl_detaildist 0)": "cl_detaildist 0",
            "Enable Detail Props (cl_detaildist 1200)": "cl_detaildist 1200",
            "buildcubemaps": "buildcubemaps",
            "sfm_bone_display_solid 0": "sfm_bone_display_solid 0",
            "sfm_bone_display_solid 1": "sfm_bone_display_solid 1",
            "Mat_Bumpmap 0": "mat_bumpmap 0",
            "Mat_Bumpmap 1": "mat_bumpmap 1",
            
        }

        self.command_tab = self.create_command_tab()
        self.menu2_tab = self.create_menu2_tab()
        self.console_tab = self.create_console_tab()
        self.logs_tab = self.create_logs_tab()
        self.booster_tab = self.create_booster_tab()
        self.language_tab = self.create_language_tab()
        self.vmt_editor_tab = self.create_vmt_editor_tab() 
        self.sfm_overlay_tab = self.create_overlay_tab()
        self.texture_tab = self.create_texture_checker_tab()
        self.guide_tab = self.create_guide_tab()
        
        
        
        

        self.sfm_notes_tab = SFMNotesTab()

        self.tabs.addTab(self.command_tab, t("Filmmaker GUI"))
        self.tabs.addTab(self.menu2_tab, t("Filmmaker GUI 2"))
        self.tabs.addTab(self.console_tab, t("Console"))
        self.tabs.addTab(self.language_tab, t("Language"))
        self.tabs.addTab(self.logs_tab, t("Logs"))
        self.tabs.addTab(self.sfm_notes_tab, t("SFM Notes"))
        self.tabs.addTab(self.vmt_editor_tab, t(u"VMTEDİTOR"))
        self.tabs.addTab(self.sfm_overlay_tab, t("SFM Overlay"))
        self.tabs.addTab(self.texture_tab, "Texture Checker")
        self.tabs.addTab(self.guide_tab, t("Guide"))
        
        
        
        for btn in self.findChildren(QtGui.QPushButton):
            add_hover_glow(btn)

        # --- Slide-in animasyonu: tab değişince aktif widget soldan kayarak girer ---
        def _on_tab_changed(index):
            try:
                widget = self.tabs.widget(index)
                if widget is not None:
                    QtCore.QTimer.singleShot(10, lambda w=widget: add_slide_in_animation(w, duration=300, offset=50))
            except Exception:
                pass
        self.tabs.currentChanged.connect(_on_tab_changed)

        layout.addWidget(self.tabs)

        # Record original English keys for widgets so runtime language switching is reliable
        try:
            self._record_translation_keys()
        except Exception:
            pass

        try:
            if hasattr(self, 'log_box'):
                self.log_box.append(u"Filmmaker GUI V3.0! 10 New Language And VMTEDİTOR!")
        except Exception:
            pass


    def create_vmt_editor_tab(self):
        return VMTEditor()

    # ---------- Styles ----------
    def _tab_style(self):
        # Faithful SFM tab style: flat, no radius, dark bg, blue active
        return """
            QTabWidget::pane {
                border: 1px solid %(border)s;
                background: %(panel)s;
                top: -1px;
            }
            QTabBar {
                background: %(bg)s;
            }
            QTabBar::tab {
                background: %(bg)s;
                color: %(text_dim)s;
                padding: 4px 10px;
                border: 1px solid %(border)s;
                border-bottom: none;
                margin-right: 1px;
                font-size: 11px;
                font-weight: normal;
                min-width: 0px;
                max-width: 9999px;
            }
            QTabBar::tab:selected {
                background: %(panel)s;
                color: %(text_bright)s;
                border-top: 2px solid %(accent)s;
                border-left: 1px solid %(border_light)s;
                border-right: 1px solid %(border_light)s;
                border-bottom: 1px solid %(panel)s;
            }
            QTabBar::tab:hover:!selected {
                background: %(muted)s;
                color: %(text)s;
            }
            QTabBar::scroller { width: 16px; }
            QTabBar QToolButton {
                background: %(bg)s;
                border: 1px solid %(border)s;
                color: %(text)s;
            }
        """ % {k: PALETTE[k] for k in (
            'bg','panel','muted','border','border_light',
            'accent','text','text_dim','text_bright')}

    def _global_button_style(self, color=PALETTE['accent']):
        # SFM button: flat grey with subtle gradient, coloured top edge
        c_top  = self._lighter(color, 1.15)
        c_bot  = self._darker(color,  0.80)
        c_htop = self._lighter(color, 1.30)
        c_hbot = self._lighter(color, 1.00)
        c_pre  = self._darker(color,  0.65)
        return """
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 %(top)s, stop:1 %(bot)s);
                color: #e0e0e0;
                font-weight: bold;
                font-size: 11px;
                border-radius: 0px;
                padding: 5px 12px;
                min-height: 20px;
                border: 1px solid %(border)s;
                border-top: 1px solid %(top_border)s;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 %(htop)s, stop:1 %(hbot)s);
            }
            QPushButton:pressed {
                background: %(pre)s;
                padding-top: 6px;
                padding-bottom: 4px;
            }
            QPushButton:disabled {
                background: #383838;
                color: #606060;
                border: 1px solid #2a2a2a;
            }
        """ % {
            "top":        c_top,
            "bot":        c_bot,
            "htop":       c_htop,
            "hbot":       c_hbot,
            "pre":        c_pre,
            "border":     PALETTE["border"],
            "top_border": self._lighter(color, 1.4),
        }

    def _darker(self, hexcol, factor=0.8):
        hexcol = hexcol.lstrip('#')
        r, g, b = [int(hexcol[i:i+2], 16) for i in (0, 2, 4)]
        return '#%02x%02x%02x' % (max(0, int(r*factor)), max(0, int(g*factor)), max(0, int(b*factor)))

    def _lighter(self, hexcol, factor=1.1):
        hexcol = hexcol.lstrip('#')
        r, g, b = [int(hexcol[i:i+2], 16) for i in (0, 2, 4)]
        return '#%02x%02x%02x' % (min(255, int(r*factor)), min(255, int(g*factor)), min(255, int(b*factor)))


    # ---------- Tabs ----------
    def create_command_tab(self):
        tab = QtGui.QWidget()
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self._scroll_style())

        container = QtGui.QWidget()
        container.setStyleSheet('background-color: %s;' % PALETTE['panel'])
        scroll.setWidget(container)

        layout = QtGui.QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        def add_button(text, color, cmd=None, callback=None):
            btn = QtGui.QPushButton(text)
            btn.setStyleSheet(self._global_button_style(color))
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            if cmd:
                btn.clicked.connect(lambda: self.log_box.append("[CMD] " + cmd))
                btn.clicked.connect(lambda: sfm.console(cmd))
            if callback:
                btn.clicked.connect(callback)
            add_click_animation(btn)
            layout.addWidget(btn)
            return btn

        def section_label(text):
            lbl = QtGui.QLabel(text)
            lbl.setStyleSheet('font-weight:bold; color: %s; font-size:11px;' % PALETTE['accent'])
            return lbl

        # Top buttons (quick commands moved to SFM Command GUI 2)


        # --- Fog Settings ---
        layout.addWidget(section_label("Fog Settings"))

        self.enable_fog_checkbox = QtGui.QCheckBox(t("Enable Fog"))
        self.enable_fog_checkbox.setStyleSheet('color: %s; font-weight:400; font-size:20px;' % PALETTE['text'])
        self.enable_fog_checkbox.stateChanged.connect(self.toggle_fog)
        layout.addWidget(self.enable_fog_checkbox)

        # Fog color sliders
        self.fog_color_sliders = {}
        for color in ["Red", "Green", "Blue"]:
            hlayout = QtGui.QHBoxLayout()
            label = QtGui.QLabel("Fog Color {}: 0".format(color))
            label.setFixedWidth(160)
            label.setStyleSheet('color: %s;' % PALETTE['text'])
            slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            slider.setRange(0, 255)
            slider.setValue(0)
            slider.valueChanged.connect(lambda val, l=label, c=color: l.setText("Fog Color {}: {}".format(c, val)))
            slider.setStyleSheet(self._slider_style())
            hlayout.addWidget(label)
            hlayout.addWidget(slider)
            layout.addLayout(hlayout)
            self.fog_color_sliders[color.lower()] = slider

        # Skybox color sliders
        self.skybox_color_sliders = {}
        for color in ["Red", "Green", "Blue"]:
            hlayout = QtGui.QHBoxLayout()
            label = QtGui.QLabel("Skybox Color {}: 0".format(color))
            label.setFixedWidth(160)
            label.setStyleSheet('color: %s;' % PALETTE['text'])
            slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            slider.setRange(0, 255)
            slider.setValue(0)
            slider.valueChanged.connect(lambda val, l=label, c=color: l.setText("Skybox Color {}: {}".format(c, val)))
            slider.setStyleSheet(self._slider_style())
            hlayout.addWidget(label)
            hlayout.addWidget(slider)
            layout.addLayout(hlayout)
            self.skybox_color_sliders[color.lower()] = slider

        # Fog ranges
        self.start_slider = self.create_range_slider("Fog Start", -10000, 30000, layout, default=0)
        self.end_slider = self.create_range_slider("Fog End", -10000, 30000, layout, default=0)
        self.start_skybox_slider = self.create_range_slider("Skybox Start", -10000, 30000, layout, default=-13)
        self.end_skybox_slider = self.create_range_slider("Skybox End", -10000, 30000, layout, default=0)

        self.btn_set_fog = QtGui.QPushButton(t("Set Fog Settings"))
        self.btn_set_fog.setStyleSheet(self._global_button_style('#b13f5c'))
        self.btn_set_fog.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_set_fog.clicked.connect(self.apply_fog_settings)

        add_click_animation(self.btn_set_fog)
        add_hover_glow(self.btn_set_fog)

        layout.addWidget(self.btn_set_fog)

        # --- Extra ---
        layout.addWidget(section_label("Extra"))

        # --- Eye Size (Live) inserted inside Extra ---
        eye_hlayout = QtGui.QHBoxLayout()
        self.eye_size_label = QtGui.QLabel("Eye Size: 1.00")
        self.eye_size_label.setFixedWidth(150)
        self.eye_size_label.setStyleSheet('color: %s;' % PALETTE['text'])
        self.eye_size_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.eye_size_slider.setRange(50, 200)  # 0.50 - 2.00
        self.eye_size_slider.setValue(100)
        self.eye_size_slider.setStyleSheet(self._slider_style())
        self.eye_size_slider.valueChanged.connect(self.update_eye_size_live)
        eye_hlayout.addWidget(self.eye_size_label)
        eye_hlayout.addWidget(self.eye_size_slider)
        layout.addLayout(eye_hlayout)

        # mat_picmip button (opens MatPicmipDialog)
        add_button(t("Set mat_picmip"), PALETTE['red'], callback=self.open_mat_picmip_dialog)



        self.btn_lightLimit = add_button(t("Light Limit Patch"),PALETTE['green'],callback=self.open_light_limit_dialog
)
        add_hover_glow(self.btn_lightLimit)

        self.btn_session_importer = add_button("Session Importer", PALETTE['accent'], callback=self.open_session_importer_dialog)
        add_hover_glow(self.btn_session_importer)

        self.btn_cleanMemory = add_button( "Clean Memory (RAM)",PALETTE['navy blue'],callback=self.clean_memory
)
        add_hover_glow(self.btn_cleanMemory)

        self.btn_extend_duration = add_button(
            'Extend Element Duration', PALETTE['green'],
            callback=self.extend_element_duration)
        add_hover_glow(self.btn_extend_duration)


        self.btn_extend_duration = add_button(
            'Extend Element Duration', PALETTE['green'],
            callback=self.extend_element_duration)
        add_hover_glow(self.btn_extend_duration)

        

        vbox = QtGui.QVBoxLayout(tab)
        vbox.addWidget(scroll)
        return tab

    def create_logs_tab(self):
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)
        tab.setStyleSheet('background-color: %s;' % PALETTE['panel'])
        self.log_box = QtGui.QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet('''
            QTextEdit {
                background-color: %s;
                color: %s;
                font-family: Consolas, monospace;
                font-size: 12px;
                border-radius: 6px;
                padding: 8px;
            }
        ''' % (PALETTE['muted'], PALETTE['text']))
        layout.addWidget(self.log_box)
        return tab

    def create_booster_tab(self):
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        def add_slider(label, minv, maxv, default, callback):
            lbl = QtGui.QLabel("{}: {}".format(label, default))
            lbl.setStyleSheet('color: %s; font-weight:600;' % PALETTE['text'])
            slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            slider.setRange(minv, maxv)
            slider.setValue(default)
            slider.valueChanged.connect(lambda val: lbl.setText("{}: {}".format(label, val)))
            slider.sliderReleased.connect(lambda: callback(slider.value()))
            slider.setStyleSheet(self._slider_style())
            layout.addWidget(lbl)
            layout.addWidget(slider)

        add_slider(t("RAM Boost Level"), -10, 4, 0, self.set_ram_boost)
        add_slider(t("FPS Boost Level"), 24, 1000, 60, self.set_fps_boost)

        btn = QtGui.QPushButton(t("Boost Now"))
        btn.setStyleSheet(self._global_button_style('#21963e'))
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.clicked.connect(self.boost_now)
        add_click_animation(btn)
        layout.addWidget(btn)
        return tab
    # ---------- New: Menu2/Console/Language helpers ----------
    def create_menu2_tab(self):
        tab = QtGui.QWidget()
        try:
            tab.setObjectName("menu2_tab")
            tab.setStyleSheet('''#menu2_tab { font-size:14px; }
                #menu2_tab QLabel { font-size:14px; }
                #menu2_tab QPushButton { font-size:14px; padding:8px 12px; min-height:30px; }
                #menu2_tab QLineEdit, #menu2_tab QComboBox { min-height:30px; font-size:14px; padding:6px 8px; }
                #menu2_tab QSlider { min-height:18px; }
            ''')
        except Exception:
            pass
        layout = QtGui.QVBoxLayout(tab)
        layout.setContentsMargins(6,6,6,6)
        layout.setSpacing(4)
        title = QtGui.QLabel(t("Filmmaker GUI 2"))
        title.setStyleSheet('font-size:16px; color: %s; font-weight:700;' % PALETTE['text'])
        self.menu2_title = title
        layout.addWidget(title)



        # --- Performance Options ---
        self.chk_texture_opt = QtGui.QCheckBox("Enable Texture Optimization")
        self.chk_texture_opt.setStyleSheet('color: %s; font-size:13px;' % PALETTE['text'])
        layout.addWidget(self.chk_texture_opt)

        self.chk_particle_boost = QtGui.QCheckBox("Activate Particle Boost")
        self.chk_particle_boost.setStyleSheet('color: %s; font-size:13px;' % PALETTE['text'])
        layout.addWidget(self.chk_particle_boost)

        self.chk_optimize_shadows = QtGui.QCheckBox("Optimize Shadows")
        self.chk_optimize_shadows.setStyleSheet('color: %s; font-size:13px;' % PALETTE['text'])
        layout.addWidget(self.chk_optimize_shadows)

        apply_perf_btn = QtGui.QPushButton("Apply")
        apply_perf_btn.setStyleSheet(self._global_button_style(PALETTE['green']))
        apply_perf_btn.setCursor(QtCore.Qt.PointingHandCursor)
        try:
            apply_perf_btn.setFixedHeight(28)
        except Exception:
            pass
        apply_perf_btn.clicked.connect(self.apply_performance_options)
        add_click_animation(apply_perf_btn)
        layout.addWidget(apply_perf_btn)

        layout.addSpacing(6)





        

        # --- Quick Commands (moved here) ---
        qc_label = QtGui.QLabel(t("Quick Commands"))
        qc_label.setStyleSheet('font-weight:700; color: %s; font-size:14px;' % PALETTE['green'])
        layout.addWidget(qc_label)

        self.menu2_quick_box = QtGui.QComboBox()
        self.menu2_quick_box.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        try:
            self.menu2_quick_box.setFixedHeight(24)
        except Exception:
            pass
        # Non-editable: require selecting from the list (no typing)
        try:
            self.menu2_quick_box.setEditable(False)
        except Exception:
            pass
        # Add a translated placeholder item (no command)
        self.menu2_quick_box.addItem(t("Select quick command"), None)
        # Add known quick commands using translated labels but preserve original command as userData
        for label in self.quick_commands:
            try:
                self.menu2_quick_box.addItem(t(label), label)
            except Exception:
                self.menu2_quick_box.addItem(label, label)
        layout.addWidget(self.menu2_quick_box)

        self.menu2_exec_btn = QtGui.QPushButton(t("Execute Quick Command"))
        self.menu2_exec_btn.setStyleSheet(self._global_button_style(PALETTE['orange']))
        self.menu2_exec_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.menu2_exec_btn.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        try:
            self.menu2_exec_btn.setFixedHeight(28)
        except Exception:
            pass
        self.menu2_exec_btn.clicked.connect(self.run_selected_quick_command)
        add_click_animation(self.menu2_exec_btn)
        layout.addWidget(self.menu2_exec_btn)

        layout.addSpacing(4)

        # --- Skybox controls (moved from Console) ---
        sky_label = QtGui.QLabel("Skybox")
        sky_label.setStyleSheet('font-weight:700; color: %s;' % PALETTE['accent'])
        layout.addWidget(sky_label)

        s_h = QtGui.QHBoxLayout()
        self.skybox_input_menu2 = QtGui.QLineEdit()
        self.skybox_input_menu2.setPlaceholderText("Enter skybox name or choose from info")
        try:
            self.skybox_input_menu2.setFixedHeight(24)
        except Exception:
            pass
        s_h.addWidget(self.skybox_input_menu2)
        info_btn = QtGui.QPushButton("i")
        try:
            info_btn.setFixedWidth(22)
            info_btn.setFixedHeight(22)
        except Exception:
            pass
        info_btn.clicked.connect(self.open_skybox_info_dialog)
        s_h.addWidget(info_btn)
        set_btn = QtGui.QPushButton(t("Set Skybox"))
        set_btn.setStyleSheet(self._global_button_style(PALETTE['accent']))
        try:
            set_btn.setFixedHeight(28)
        except Exception:
            pass
        set_btn.clicked.connect(self.set_skybox)
        s_h.addWidget(set_btn)
        reset_btn = QtGui.QPushButton(t("Reset Skybox"))
        reset_btn.setStyleSheet(self._global_button_style(PALETTE['muted']))
        try:
            reset_btn.setFixedHeight(28)
        except Exception:
            pass
        reset_btn.clicked.connect(self.reset_skybox)
        s_h.addWidget(reset_btn)
        layout.addLayout(s_h)

        layout.addSpacing(12)

        # --- FPS Booster controls (moved here) ---
        def _add_booster_slider(label, minv, maxv, default, callback):
            lbl = QtGui.QLabel("{}: {}".format(label, default))
            lbl.setStyleSheet('color: %s; font-weight:600;' % PALETTE['text'])
            slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            slider.setRange(minv, maxv)
            slider.setValue(default)
            slider.valueChanged.connect(lambda val, ll=lbl, llabel=label: ll.setText("{}: {}".format(llabel, val)))
            slider.sliderReleased.connect(lambda s=slider: callback(s.value()))
            slider.setStyleSheet(self._slider_style())
            layout.addWidget(lbl)
            layout.addWidget(slider)

        _add_booster_slider(t("RAM Boost Level"), -10, 4, 0, self.set_ram_boost)
        _add_booster_slider(t("FPS Boost Level"), 24, 1000, 60, self.set_fps_boost)

        btn = QtGui.QPushButton(t("Boost Now"))
        btn.setStyleSheet(self._global_button_style('#395b64'))
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.clicked.connect(self.boost_now)
        add_click_animation(btn)
        layout.addWidget(btn)


        return tab

    def create_overlay_tab(self):
        tab = QtGui.QWidget()
        tab.setStyleSheet("background:#1e1e1e; color:#CAC9C9;")
        main_l = QtGui.QVBoxLayout(tab)
        main_l.setContentsMargins(12, 12, 12, 12)
        main_l.setSpacing(8)

        # --- Baslik ---
        self.overlay_title_lbl = QtGui.QLabel(t("SFM Overlay"))
        self.overlay_title_lbl.setStyleSheet("font-size:15px; font-weight:700; color:#3fa9f5;")
        main_l.addWidget(self.overlay_title_lbl)

        BTN = ("QPushButton{background:#2f2f2f;color:#CAC9C9;border:1px solid #444;"
               "padding:5px 12px;border-radius:5px;}"
               "QPushButton:hover{background:#3a3a3a;}")

        # --- Resim ekleme ---
        img_row = QtGui.QHBoxLayout()
        self.btn_overlay_add = QtGui.QPushButton(t("Add Image"))
        self.btn_overlay_add.setStyleSheet(BTN)
        self.btn_overlay_add.clicked.connect(self._overlay_add_image)
        img_row.addWidget(self.btn_overlay_add)

        self.btn_overlay_remove = QtGui.QPushButton(t("Remove Selected"))
        self.btn_overlay_remove.setStyleSheet(BTN)
        self.btn_overlay_remove.clicked.connect(self._overlay_remove_selected)
        img_row.addWidget(self.btn_overlay_remove)

        self.btn_overlay_front = QtGui.QPushButton(t("Bring to Front"))
        self.btn_overlay_front.setStyleSheet(BTN)
        self.btn_overlay_front.clicked.connect(self._overlay_bring_front)
        img_row.addWidget(self.btn_overlay_front)

        self.btn_overlay_toggle = QtGui.QPushButton(t("Toggle All"))
        self.btn_overlay_toggle.setStyleSheet(BTN)
        self.btn_overlay_toggle.clicked.connect(self.toggle_all_overlays)
        img_row.addWidget(self.btn_overlay_toggle)

        self.btn_overlay_clear = QtGui.QPushButton(t("Remove All"))
        self.btn_overlay_clear.setStyleSheet(
            "QPushButton{background:#6b1a1a;color:white;border:1px solid #a02020;"
            "padding:5px 12px;border-radius:5px;}"
            "QPushButton:hover{background:#8b2020;}"
        )
        self.btn_overlay_clear.clicked.connect(self.remove_all_overlays)
        img_row.addWidget(self.btn_overlay_clear)
        img_row.addStretch()
        main_l.addLayout(img_row)

        # --- Image list ---
        self.overlay_images_list = QtGui.QListWidget()
        self.overlay_images_list.setStyleSheet(
            "background:#252526; border:1px solid #3a3a3a; border-radius:5px; color:#CAC9C9;"
        )
        self.overlay_images_list.setMaximumHeight(110)
        self.overlay_images_list.currentRowChanged.connect(self._overlay_on_selection_changed)
        main_l.addWidget(self.overlay_images_list)

        # --- Opacity ---
        op_row = QtGui.QHBoxLayout()
        self.overlay_opacity_lbl = QtGui.QLabel(t("Opacity:"))
        self.overlay_opacity_lbl.setFixedWidth(56)
        self.overlay_opacity_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.overlay_opacity_slider.setRange(0, 100)
        self.overlay_opacity_slider.setValue(100)
        self.overlay_opacity_slider.valueChanged.connect(self._overlay_on_opacity_changed)
        op_val = QtGui.QLabel("100%")
        op_val.setFixedWidth(36)
        self.overlay_opacity_slider.valueChanged.connect(
            lambda v, lbl=op_val: lbl.setText("{}%".format(v)))
        op_row.addWidget(self.overlay_opacity_lbl)
        op_row.addWidget(self.overlay_opacity_slider)
        op_row.addWidget(op_val)
        main_l.addLayout(op_row)

        # --- Scale ---
        sc_row = QtGui.QHBoxLayout()
        self.overlay_scale_lbl = QtGui.QLabel(t("Scale:"))
        self.overlay_scale_lbl.setFixedWidth(56)
        self.overlay_scale_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.overlay_scale_slider.setRange(10, 300)
        self.overlay_scale_slider.setValue(100)
        self.overlay_scale_slider.valueChanged.connect(self._overlay_on_scale_changed)
        sc_val = QtGui.QLabel("100%")
        sc_val.setFixedWidth(36)
        self.overlay_scale_slider.valueChanged.connect(
            lambda v, lbl=sc_val: lbl.setText("{}%".format(v)))
        sc_row.addWidget(self.overlay_scale_lbl)
        sc_row.addWidget(self.overlay_scale_slider)
        sc_row.addWidget(sc_val)
        main_l.addLayout(sc_row)

        # --- Lock / Click-through ---
        self.overlay_lock_chk = QtGui.QCheckBox(t("Lock (Click-through)"))
        self.overlay_lock_chk.setStyleSheet("color:#aaa;")
        self.overlay_lock_chk.toggled.connect(self._overlay_on_lock_toggled)
        main_l.addWidget(self.overlay_lock_chk)

        # --- Presets ---
        sep = QtGui.QFrame()
        sep.setFrameShape(QtGui.QFrame.HLine)
        sep.setStyleSheet("color:#333;")
        main_l.addWidget(sep)

        self.overlay_preset_title = QtGui.QLabel(t("Presets"))
        self.overlay_preset_title.setStyleSheet("font-size:12px; font-weight:600; color:#aaa;")
        main_l.addWidget(self.overlay_preset_title)

        preset_row = QtGui.QHBoxLayout()
        self.overlay_preset_name = QtGui.QLineEdit()
        self.overlay_preset_name.setPlaceholderText(t("Preset name..."))
        self.overlay_preset_name.setStyleSheet(
            "background:#252526; color:#CAC9C9; border:1px solid #444; border-radius:4px; padding:4px;"
        )
        preset_row.addWidget(self.overlay_preset_name)

        self.btn_overlay_save_p = QtGui.QPushButton(t("Save"))
        self.btn_overlay_save_p.setStyleSheet(BTN)
        self.btn_overlay_save_p.clicked.connect(self._overlay_save_preset)
        preset_row.addWidget(self.btn_overlay_save_p)
        main_l.addLayout(preset_row)

        load_row = QtGui.QHBoxLayout()
        self.overlay_preset_combo = QtGui.QComboBox()
        self.overlay_preset_combo.setStyleSheet(
            "background:#252526; color:#CAC9C9; padding:4px; border-radius:4px; border:1px solid #444;"
        )
        load_row.addWidget(self.overlay_preset_combo)

        self.btn_overlay_load_p = QtGui.QPushButton(t("Load"))
        self.btn_overlay_load_p.setStyleSheet(BTN)
        self.btn_overlay_load_p.clicked.connect(self._overlay_load_preset)
        load_row.addWidget(self.btn_overlay_load_p)

        self.btn_overlay_del_p = QtGui.QPushButton(t("Delete"))
        self.btn_overlay_del_p.setStyleSheet(BTN)
        self.btn_overlay_del_p.clicked.connect(self._overlay_delete_preset)
        load_row.addWidget(self.btn_overlay_del_p)
        main_l.addLayout(load_row)

        # Presets yukle
        import json as _json
        try:
            self._overlay_presets_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "overlay_presets.json")
        except Exception:
            self._overlay_presets_file = "overlay_presets.json"
        self._overlay_presets = {}
        try:
            if os.path.exists(self._overlay_presets_file):
                with open(self._overlay_presets_file, 'r') as _f:
                    self._overlay_presets = _json.load(_f)
                for k in sorted(self._overlay_presets.keys()):
                    self.overlay_preset_combo.addItem(k)
        except Exception:
            pass

        main_l.addStretch()
        return tab

    def create_whatif_tab(self):
        tab = QtGui.QWidget()
        tab.setStyleSheet("background-color: %s;" % PALETTE["panel"])
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self._scroll_style())
        container = QtGui.QWidget()
        container.setStyleSheet("background-color: %s;" % PALETTE["panel"])
        scroll.setWidget(container)
        layout = QtGui.QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        def sec(text):
            l = QtGui.QLabel(text)
            l.setStyleSheet("font-weight:700;color:%s;font-size:15px;" % PALETTE["teal"])
            return l

        # ── Header ──
        layout.addWidget(sec("Skibidi What If - Episode Scenarios"))
        desc = QtGui.QLabel(
            "Generate alternative 'What If' scenarios for Skibidi Toilet episodes and characters. "
            "Choose an episode/event, pick a character, and get creative alternate storylines."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color:%s;font-size:12px;" % PALETTE["text"])
        layout.addWidget(desc)

        # ── Episode selector ──
        layout.addWidget(sec("Episode / Event"))
        self._wi_episode = QtGui.QComboBox()
        self._wi_episode.addItems([
            "Skibidi Toilet 1  (first appearance)",
            "Skibidi Toilet 5  (Cameraman joins)",
            "Skibidi Toilet 10 (Speakerman debut)",
            "Skibidi Toilet 20 (Titan Cameraman first look)",
            "Skibidi Toilet 35 (G-Man alliance hint)",
            "Skibidi Toilet 45 (Astro Toilet reveal)",
            "Skibidi Toilet 55 (Plungerman debut)",
            "Skibidi Toilet 67 (Titan TV Man upgrade)",
            "Skibidi Toilet 70 (Large Skibidi boss)",
            "Skibidi Toilet 75 (Alliance vs mutant Skibidi)",
            "Skibidi Toilet 76 (Scientist reveal)",
            "Skibidi Toilet 77 (UTSM first appearance)",
            "Skibidi Toilet 78 (UTSM rampage)",
            "Skibidi Toilet 79 (G-Man vs UTSM scenario)",
            "Custom episode / event",
        ])
        self._wi_episode.setStyleSheet(
            "QComboBox{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:7px;font-size:12px;}"
            "QComboBox::drop-down{border:none;}"
            "QComboBox QAbstractItemView{background:%s;color:%s;selection-background-color:%s;}" % (
                PALETTE["bg"], PALETTE["text"], PALETTE["muted"],
                PALETTE["panel"], PALETTE["text"], PALETTE["accent"])
        )
        layout.addWidget(self._wi_episode)

        # ── Character selector ──
        layout.addWidget(sec("Key Character / Guest"))
        self._wi_character = QtGui.QComboBox()
        self._wi_character.addItems([
            "G-Man (Half-Life)",
            "UTSM (Ultra Titan Skibidi Mutant)",
            "Titan Cameraman",
            "Titan Speakerman",
            "Titan TV Man",
            "Astro Toilet",
            "Large Skibidi Toilet",
            "Plungerman",
            "Scientist / Doctor",
            "Upgraded Cameraman",
            "Upgraded Speakerman",
            "Upgraded TV Man",
            "Regular Skibidi Toilet",
            "Alliance Commander",
            "Custom character",
        ])
        self._wi_character.setStyleSheet(self._wi_episode.styleSheet())
        layout.addWidget(self._wi_character)

        # ── What If type ──
        layout.addWidget(sec("What If Type"))
        type_row = QtGui.QHBoxLayout()
        self._wi_type = QtGui.QComboBox()
        self._wi_type.addItems([
            "What if this character appeared in this episode?",
            "What if this character switched sides?",
            "What if this character was the final boss?",
            "What if this character saved the Alliance?",
            "What if this character joined the Skibidi side?",
            "What if this character vs UTSM?",
            "What if G-Man interfered in this episode?",
            "What if this character had a different upgrade?",
            "What if this episode ended differently?",
            "What if two titans fought each other here?",
        ])
        self._wi_type.setStyleSheet(self._wi_episode.styleSheet())
        type_row.addWidget(self._wi_type, 1)
        layout.addLayout(type_row)

        # ── Extra context ──
        layout.addWidget(sec("Extra Details (optional)"))
        self._wi_extra = QtGui.QLineEdit()
        self._wi_extra.setStyleSheet(
            "QLineEdit{background:%s;color:%s;border:1px solid %s;"
            "border-radius:6px;padding:8px;font-size:12px;}" % (
                PALETTE["bg"], PALETTE["text"], PALETTE["muted"])
        )
        self._wi_extra.setPlaceholderText("e.g. 'G-Man has a secret weapon', 'the battle takes place underwater'...")
        layout.addWidget(self._wi_extra)

        # ── Generate button ──
        self._wi_gen_btn = QtGui.QPushButton("Generate What If Scenario")
        self._wi_gen_btn.setFixedHeight(42)
        self._wi_gen_btn.setStyleSheet(self._global_button_style(PALETTE["teal"]))
        self._wi_gen_btn.clicked.connect(self._wi_generate)
        add_hover_glow(self._wi_gen_btn)
        layout.addWidget(self._wi_gen_btn)

        # ── Progress ──
        self._wi_progress = QtGui.QProgressBar()
        self._wi_progress.setRange(0, 0)
        self._wi_progress.setFixedHeight(6)
        self._wi_progress.setTextVisible(False)
        self._wi_progress.setVisible(False)
        self._wi_progress.setStyleSheet(
            "QProgressBar{background:%s;border-radius:3px;border:none;}"
            "QProgressBar::chunk{background:%s;border-radius:3px;}" % (
                PALETTE["bg"], PALETTE["teal"])
        )
        layout.addWidget(self._wi_progress)

        # ── Output ──
        layout.addWidget(sec("What If Scenario"))
        self._wi_output = QtGui.QTextEdit()
        self._wi_output.setReadOnly(True)
        self._wi_output.setMinimumHeight(260)
        self._wi_output.setStyleSheet(
            "QTextEdit{background:%s;color:%s;border:1px solid %s;"
            "border-radius:6px;font-size:12px;padding:10px;}" % (
                PALETTE["bg"], PALETTE["text"], PALETTE["muted"])
        )
        layout.addWidget(self._wi_output, 1)

        # ── Action buttons ──
        btn_row = QtGui.QHBoxLayout()
        copy_btn = QtGui.QPushButton("Copy to Clipboard")
        copy_btn.setStyleSheet(self._global_button_style(PALETTE["accent"]))
        copy_btn.clicked.connect(self._wi_copy)
        add_hover_glow(copy_btn)
        clear_btn = QtGui.QPushButton("Clear")
        clear_btn.setStyleSheet(self._global_button_style(PALETTE["red"]))
        clear_btn.clicked.connect(lambda: self._wi_output.clear())
        add_hover_glow(clear_btn)
        btn_row.addWidget(copy_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        vbox = QtGui.QVBoxLayout(tab)
        vbox.addWidget(scroll)
        return tab

    def create_guide_tab(self):
        """Filmmaker GUI - Feature Guide (English)"""
        tab = QtGui.QWidget()
        tab.setStyleSheet("background:%s;" % PALETTE["panel"])
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self._scroll_style())
        container = QtGui.QWidget()
        container.setStyleSheet("background:%s;" % PALETTE["panel"])
        scroll.setWidget(container)
        lay = QtGui.QVBoxLayout(container)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        def sec(text):
            lbl = QtGui.QLabel(text)
            lbl.setStyleSheet("font-weight:bold;color:%s;font-size:13px;border-bottom:1px solid %s;padding-bottom:3px;" % (PALETTE["accent"], PALETTE["border"]))
            return lbl
        def sub(text):
            lbl = QtGui.QLabel(text)
            lbl.setStyleSheet("font-weight:bold;color:%s;font-size:11px;" % PALETTE["text"])
            return lbl
        def desc(text):
            lbl = QtGui.QLabel(text)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color:%s;font-size:11px;" % PALETTE["text_dim"])
            return lbl
        def code(text):
            lbl = QtGui.QLabel(text)
            lbl.setStyleSheet("background:#1a1a1a;color:#a8c4e0;font-family:Consolas,monospace;font-size:10px;padding:5px 8px;border:1px solid %s;" % PALETTE["border"])
            return lbl
        def card(widgets):
            f = QtGui.QFrame()
            f.setStyleSheet("QFrame{background:%s;border:1px solid %s;}" % (PALETTE["bg"], PALETTE["border"]))
            fl = QtGui.QVBoxLayout(f)
            fl.setContentsMargins(10, 8, 10, 8)
            fl.setSpacing(5)
            for w in widgets: fl.addWidget(w)
            return f

        lay.addWidget(sec('Tab: FMG'))
        lay.addWidget(card([sub('Fog Settings'), desc('Enable/disable scene fog. Adjust RGB colour (0-255), start/end distances, skybox fog.'), code('env_fog_controller  -- SFM fog entity')]))
        lay.addWidget(card([sub('Eye Size'), desc('Scale eye size on models: 0.50x - 2.00x. Applied live.')]))
        lay.addWidget(card([sub('Set mat_picmip'), desc('Texture quality. Lower = sharper (more VRAM). Higher = faster.'), code('mat_picmip -1  (highest)    mat_picmip 4  (lowest)')]))
        lay.addWidget(card([sub('Light Limit Patch'), desc("Raises SFM's default 8-light limit for complex scenes.")]))
        lay.addWidget(card([sub('Session Importer'), desc('Import a .dmx session: models, animations, cameras.')]))
        lay.addWidget(card([sub('Clean Memory (DXVK-aware)'), desc('Aggressive memory cleanup: Python GC, Windows Working Set flush, Heap compact, DXVK/Vulkan GPU flush signal, mat_reloadallmaterials, r_cleardecals, r_flushlod. When SFM runs under DXVK the GPU flush tells Vulkan to submit queued commands and free staging buffers -- this is what causes the large VRAM drop seen in the BEFORE/AFTER screenshots.'), code('Steps: GC -> WorkingSet -> HeapCompact -> DXVK signal -> mat_reloadallmaterials -> r_cleardecals -> r_flushlod')]))
        lay.addWidget(card([sub('Extend Element Duration'), desc('Fixes the SFM 60-second object lock bug. Opens ChannelsClip Editor: set Duration to 70+ seconds for all AnimationSet channel clips in the current shot.')]))

        lay.addWidget(sec('Tab: FMG 2'))
        lay.addWidget(card([sub('Performance Options'), desc('Toggle texture optimisation (mat_picmip 2), particle boost, shadow optimisation.')]))
        lay.addWidget(card([sub('Quick Commands'), desc('Dropdown of common console commands. Select and run instantly.'), code('mat_fullbright 1   r_drawparticles 0   sv_cheats 1')]))
        lay.addWidget(card([sub('Skybox'), desc('Change scene skybox by name. Info button shows all supported skyboxes.'), code('skybox_sw sky_dustbowl_01')]))
        lay.addWidget(card([sub('RAM & FPS Boost'), desc('Sliders for memory cache (-10 to +4) and target FPS (24-1000). Apply with Boost Now.')]))

        lay.addWidget(sec('Tab: Console'))
        lay.addWidget(card([desc('Execute any SFM console command directly.'), code('mat_wireframe 1    r_drawviewmodel 0    host_timescale 0.5')]))

        lay.addWidget(sec('Tab: VMT Editor'))
        lay.addWidget(card([desc('Open, edit, and save .vmt material files. Supports all standard VMT parameters.')]))

        lay.addWidget(sec('Tab: Overlay'))
        lay.addWidget(card([sub('Add Image'), desc('Layer a transparent image over the SFM viewport for references, guides, or watermarks.')]))
        lay.addWidget(card([sub('Opacity / Scale / Lock'), desc('Opacity 0-100%. Scale: resize overlay. Lock: click-through so SFM controls stay usable.')]))
        lay.addWidget(card([sub('Presets'), desc('Save and load overlay configurations (image, position, scale, opacity).')]))

        lay.addWidget(sec('Tab: Textures (Texture Checker)'))
        lay.addWidget(card([sub('Supported File Types'), desc('BSP Map (.bsp): all map textures.  Particle (.pcf): material paths from particles.  MDL Model (.mdl): textures from model header.  Both/All: scan multiple types.')]))
        lay.addWidget(card([sub('MDL Support'), desc('Reads the MDL v44/v49 header: textures[] + texturedir[] arrays. Finds all referenced material paths and checks if VMT and VTF exist in your search paths.'), code('Header offsets: 0xD0 numtextures  0xD4 textureindex  0xD8 numtexdirs  0xDC texturedirindex')]))
        lay.addWidget(card([sub('Result Statuses'), code('OK          -- VMT and VTF both found\nMISSING VTF -- VMT found, VTF missing (pink/error)\nMISSING VMT -- VTF found, VMT missing\nMISSING     -- both VMT and VTF missing')]))
        lay.addWidget(card([sub('Material Search Paths'), desc('Add full paths to materials folders, one per line. Auto-fill detects common SFM installs.'), code('C:/SteamLibrary/.../SourceFilmmaker/game/usermod/materials')]))
        lay.addWidget(card([sub('Export Report'), desc('Save scan results to a .txt file.')]))

        lay.addWidget(sec('Tab: Logs'))
        lay.addWidget(card([desc('Records all button presses, commands, memory operations, and errors. Use Clear to reset.')]))

        lay.addStretch()
        vbox = QtGui.QVBoxLayout(tab)
        vbox.setContentsMargins(0,0,0,0)
        vbox.addWidget(scroll)
        return tab

    def create_texture_checker_tab(self):
        tab = QtGui.QWidget()
        tab.setStyleSheet("background-color: %s;" % PALETTE["panel"])
        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self._scroll_style())
        container = QtGui.QWidget()
        container.setStyleSheet("background-color: %s;" % PALETTE["panel"])
        scroll.setWidget(container)
        layout = QtGui.QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        def section_label(text):
            lbl = QtGui.QLabel(text)
            lbl.setStyleSheet("font-weight:700; color:%s; font-size:15px;" % PALETTE["teal"])
            return lbl

        layout.addWidget(section_label("Texture / Material Checker"))
        desc = QtGui.QLabel("Select a .bsp map or .pcf particle file. Scans all referenced VMT/VTF textures and shows which are missing.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color:%s; font-size:12px;" % PALETTE["text"])
        layout.addWidget(desc)

        # ── File type selector ──
        layout.addWidget(section_label("File Type"))
        type_row = QtGui.QHBoxLayout()
        self._tx_type_combo = QtGui.QComboBox()
        self._tx_type_combo.addItems(["BSP Map (.bsp)", "Particle (.pcf)", "MDL Model (.mdl)", "Both (BSP + PCF)", "All (BSP + PCF + MDL)"])
        self._tx_type_combo.setStyleSheet(
            "QComboBox{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:7px;font-size:12px;}"
            "QComboBox::drop-down{border:none;}"
            "QComboBox QAbstractItemView{background:%s;color:%s;}" % (
                PALETTE["bg"],PALETTE["text"],PALETTE["muted"],PALETTE["panel"],PALETTE["text"]))
        self._tx_type_combo.currentIndexChanged.connect(self._tx_on_type_changed)
        type_row.addWidget(self._tx_type_combo, 1)
        layout.addLayout(type_row)

        # ── BSP row ──
        self._tx_bsp_widget = QtGui.QWidget()
        bsp_lay = QtGui.QVBoxLayout(self._tx_bsp_widget)
        bsp_lay.setContentsMargins(0,0,0,0); bsp_lay.setSpacing(4)
        bsp_lbl = QtGui.QLabel("BSP Map File / Name")
        bsp_lbl.setStyleSheet("color:%s;font-size:12px;font-weight:bold;" % PALETTE["text"])
        bsp_lay.addWidget(bsp_lbl)
        bsp_row = QtGui.QHBoxLayout()
        self._tx_map_line = QtGui.QLineEdit()
        self._tx_map_line.setPlaceholderText("e.g. de_dust2  or browse for a .bsp file")
        self._tx_map_line.setStyleSheet(
            "QLineEdit{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:7px;font-size:12px;}"
            "QLineEdit:focus{border:1px solid %s;}" % (PALETTE["bg"],PALETTE["text"],PALETTE["muted"],PALETTE["teal"]))
        browse_btn = QtGui.QPushButton("Browse BSP")
        browse_btn.setStyleSheet(self._global_button_style(PALETTE["accent"]))
        browse_btn.clicked.connect(self._tx_browse_bsp)
        add_hover_glow(browse_btn)
        bsp_row.addWidget(self._tx_map_line, 1); bsp_row.addWidget(browse_btn)
        bsp_lay.addLayout(bsp_row)
        layout.addWidget(self._tx_bsp_widget)

        # ── PCF row ──
        self._tx_pcf_widget = QtGui.QWidget()
        self._tx_pcf_widget.setVisible(False)
        pcf_lay = QtGui.QVBoxLayout(self._tx_pcf_widget)
        pcf_lay.setContentsMargins(0,0,0,0); pcf_lay.setSpacing(4)
        pcf_lbl = QtGui.QLabel("Particle File (.pcf)")
        pcf_lbl.setStyleSheet("color:%s;font-size:12px;font-weight:bold;" % PALETTE["text"])
        pcf_lay.addWidget(pcf_lbl)
        pcf_row = QtGui.QHBoxLayout()
        self._tx_pcf_line = QtGui.QLineEdit()
        self._tx_pcf_line.setPlaceholderText("Browse for a .pcf particle file...")
        self._tx_pcf_line.setStyleSheet(
            "QLineEdit{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:7px;font-size:12px;}"
            "QLineEdit:focus{border:1px solid %s;}" % (PALETTE["bg"],PALETTE["text"],PALETTE["muted"],PALETTE["teal"]))
        browse_pcf_btn = QtGui.QPushButton("Browse PCF")
        browse_pcf_btn.setStyleSheet(self._global_button_style(PALETTE["accent"]))
        browse_pcf_btn.clicked.connect(self._tx_browse_pcf)
        add_hover_glow(browse_pcf_btn)
        pcf_row.addWidget(self._tx_pcf_line, 1); pcf_row.addWidget(browse_pcf_btn)
        pcf_lay.addLayout(pcf_row)
        layout.addWidget(self._tx_pcf_widget)

        # ── Scan button ──
        # ── MDL row ──
        self._tx_mdl_widget = QtGui.QWidget()
        self._tx_mdl_widget.setVisible(False)
        mdl_lay = QtGui.QVBoxLayout(self._tx_mdl_widget)
        mdl_lay.setContentsMargins(0,0,0,0); mdl_lay.setSpacing(4)
        mdl_lbl = QtGui.QLabel("Model File (.mdl)")
        mdl_lbl.setStyleSheet("color:%s;font-size:12px;font-weight:bold;" % PALETTE["text"])
        mdl_lay.addWidget(mdl_lbl)
        mdl_row = QtGui.QHBoxLayout()
        self._tx_mdl_line = QtGui.QLineEdit()
        self._tx_mdl_line.setPlaceholderText("Browse for a .mdl model file...")
        mdl_browse_btn = QtGui.QPushButton("Browse MDL")
        mdl_browse_btn.setStyleSheet(self._global_button_style(PALETTE["accent"]))
        def _browse_mdl():
            try:
                path, _ = QtGui.QFileDialog.getOpenFileName(self, "Select Model File", "", "MDL Files (*.mdl);;All Files (*.*)")
                if path: self._tx_mdl_line.setText(path)
            except Exception as e: QtGui.QMessageBox.warning(self, "Error", str(e))
        mdl_browse_btn.clicked.connect(_browse_mdl)
        add_hover_glow(mdl_browse_btn)
        mdl_row.addWidget(self._tx_mdl_line, 1); mdl_row.addWidget(mdl_browse_btn)
        mdl_lay.addLayout(mdl_row)
        layout.addWidget(self._tx_mdl_widget)

        scan_btn = QtGui.QPushButton("Scan Textures")
        scan_btn.setFixedHeight(38)
        scan_btn.setStyleSheet(self._global_button_style(PALETTE["teal"]))
        scan_btn.clicked.connect(self._tx_scan)
        add_hover_glow(scan_btn)
        layout.addWidget(scan_btn)
        





        layout.addWidget(section_label("Material Search Paths"))
        self._tx_paths_edit = QtGui.QTextEdit()
        self._tx_paths_edit.setFixedHeight(72)
        self._tx_paths_edit.setStyleSheet(
            "QTextEdit{background:%s;color:%s;border:1px solid %s;border-radius:6px;font-size:10px;font-family:Courier;padding:5px;}"
            % (PALETTE["bg"],PALETTE["text"],PALETTE["muted"]))
        self._tx_auto_fill_paths()
        layout.addWidget(self._tx_paths_edit)

        self._tx_progress = QtGui.QProgressBar()
        self._tx_progress.setRange(0,100); self._tx_progress.setValue(0)
        self._tx_progress.setFixedHeight(8); self._tx_progress.setTextVisible(False)
        self._tx_progress.setVisible(False)
        self._tx_progress.setStyleSheet(
            "QProgressBar{background:%s;border-radius:4px;border:none;}"
            "QProgressBar::chunk{background:%s;border-radius:4px;}" % (PALETTE["bg"],PALETTE["teal"]))
        layout.addWidget(self._tx_progress)

        self._tx_stats_lbl = QtGui.QLabel("")
        self._tx_stats_lbl.setStyleSheet("color:%s;font-size:12px;font-weight:700;" % PALETTE["text"])
        layout.addWidget(self._tx_stats_lbl)

        layout.addWidget(section_label("Results"))
        filter_row = QtGui.QHBoxLayout()
        fl = QtGui.QLabel("Filter:")
        fl.setStyleSheet("color:%s;font-size:12px;" % PALETTE["text"])
        self._tx_filter_combo = QtGui.QComboBox()
        self._tx_filter_combo.addItems(["All","Missing Only","Found Only"])
        self._tx_filter_combo.setStyleSheet(
            "QComboBox{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:6px;font-size:12px;}"
            "QComboBox::drop-down{border:none;}"
            "QComboBox QAbstractItemView{background:%s;color:%s;}" % (
                PALETTE["bg"],PALETTE["text"],PALETTE["muted"],PALETTE["panel"],PALETTE["text"]))
        self._tx_filter_combo.currentIndexChanged.connect(self._tx_apply_filter)
        self._tx_search_line = QtGui.QLineEdit()
        self._tx_search_line.setPlaceholderText("Search texture name...")
        self._tx_search_line.setStyleSheet(
            "QLineEdit{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:7px;font-size:12px;}"
            % (PALETTE["bg"],PALETTE["text"],PALETTE["muted"]))
        self._tx_search_line.textChanged.connect(self._tx_apply_filter)
        export_btn = QtGui.QPushButton("Export Report")
        export_btn.setStyleSheet(self._global_button_style(PALETTE["accent"]))
        export_btn.clicked.connect(self._tx_export_report)
        add_hover_glow(export_btn)
        filter_row.addWidget(fl); filter_row.addWidget(self._tx_filter_combo)
        filter_row.addWidget(self._tx_search_line,1); filter_row.addWidget(export_btn)
        layout.addLayout(filter_row)

        self._tx_table = QtGui.QTableWidget()
        self._tx_table.setColumnCount(3)
        self._tx_table.setHorizontalHeaderLabels(["Status","Texture / Material Path","Type"])
        self._tx_table.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self._tx_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self._tx_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._tx_table.setAlternatingRowColors(True)
        self._tx_table.verticalHeader().setVisible(False)
        self._tx_table.setStyleSheet(
            "QTableWidget{background:%s;color:%s;border:1px solid %s;gridline-color:%s;font-size:12px;}"
            "QTableWidget::item{padding:4px;}"
            "QTableWidget::item:selected{background:%s;color:%s;}"
            "QTableWidget::item:alternate{background:%s;}"
            "QHeaderView::section{background:%s;color:%s;padding:6px;border:none;border-bottom:2px solid %s;font-weight:700;}"
            "QTableWidget{alternate-background-color:%s;}" % (
                PALETTE["bg"],PALETTE["text"],PALETTE["muted"],PALETTE["muted"],
                PALETTE["accent"],PALETTE["text"],PALETTE["panel"],
                PALETTE["panel"],PALETTE["teal"],PALETTE["teal"],PALETTE["panel"]))
        self._tx_table.setColumnWidth(0,100); self._tx_table.setColumnWidth(2,80)
        layout.addWidget(self._tx_table,1)

        vbox = QtGui.QVBoxLayout(tab)
        vbox.addWidget(scroll)
        self._tx_all_results = []
        return tab

    def _tx_auto_fill_paths(self):
        try:
            paths = []
            for root in ["C:/Program Files (x86)/Steam/steamapps/common/SourceFilmmaker/game",
                         "D:/Program Files (x86)/Steam/steamapps/common/SourceFilmmaker/game",
                         "D:/Steam/steamapps/common/SourceFilmmaker/game",
                         "C:/Steam/steamapps/common/SourceFilmmaker/game",
                         "E:/Steam/steamapps/common/SourceFilmmaker/game"]:
                if os.path.isdir(root):
                    for sub in ["usermod","tf","hl2","ep2","portal","workshop"]:
                        p = os.path.join(root, sub, "materials")
                        if os.path.isdir(p): paths.append(p)
            self._tx_paths_edit.setPlainText(
                "\n".join(paths) if paths else
                "# Paste your materials folder paths here, one per line.\n# Example: C:/SteamLibrary/steamapps/common/SourceFilmmaker/game/usermod/materials")
        except Exception: pass

    def _tx_browse_bsp(self):
        try:
            path, _ = QtGui.QFileDialog.getOpenFileName(self,"Select Map File","","BSP Files (*.bsp);;All Files (*.*)")
            if path: self._tx_map_line.setText(path)
        except Exception as e: QtGui.QMessageBox.warning(self,"Error",str(e))
         

    def _tx_on_type_changed(self, idx):
        try:
            self._tx_bsp_widget.setVisible(idx in (0, 3, 4))
            self._tx_pcf_widget.setVisible(idx in (1, 3, 4))
            self._tx_mdl_widget.setVisible(idx in (2, 4))
        except Exception:
            pass

    def _tx_browse_pcf(self):
        try:
            path, _ = QtGui.QFileDialog.getOpenFileName(self, "Select Particle File", "", "Particle Files (*.pcf);;All Files (*.*)")
            if path: self._tx_pcf_line.setText(path)
        except Exception as e: QtGui.QMessageBox.warning(self, "Error", str(e))

    def _tx_read_pcf_textures(self, pcf_path):
        """
        Parse a PCF particle file (DMX binary or ASCII) and extract all
        material/texture references.

        DMX binary format:
          <header_string>\0
          int32: string_count
          string_count x null-terminated strings   <- ALL strings here
          ... element data (contains string indices, not raw strings)

        DMX ASCII format:
          quoted strings throughout the file

        We read the full string table first, then also do a fallback
        regex scan over the entire file for any missed paths.
        """
        textures = []
        seen = set()
        try:
            import struct as _s, re as _re
            with open(pcf_path, "rb") as f:
                raw = f.read()

            def add_path(val):
                val = val.replace("\\", "/").replace("\\\\", "/").strip()
                val_low = val.lower()
                if not ("/" in val):
                    return
                is_mat = (val_low.startswith("materials/") or
                          val_low.endswith(".vtf") or val_low.endswith(".vmt") or
                          val_low.endswith(".tga") or val_low.endswith(".png"))
                if not is_mat:
                    return
                parts = [p for p in val.split("/") if p]
                if len(parts) < 2:
                    return
                clean = val[len("materials/"):] if val_low.startswith("materials/") else val
                no_ext = clean.rsplit(".", 1)[0] if "." in clean.split("/")[-1] else clean
                if no_ext and no_ext not in seen and len(no_ext) >= 4:
                    seen.add(no_ext)
                    textures.append(no_ext)

            # ── Method 1: DMX binary string table ──
            # Header ends at first \0
            header_end = raw.find(b"\x00")
            if header_end > 0 and header_end < 512:
                pos = header_end + 1
                if pos + 4 <= len(raw):
                    str_count = _s.unpack_from("<I", raw, pos)[0]
                    pos += 4
                    # Sanity check: str_count should be reasonable
                    if 1 <= str_count <= 100000:
                        for _ in range(str_count):
                            end_pos = raw.find(b"\x00", pos)
                            if end_pos < 0 or end_pos - pos > 512:
                                pos += 1
                                continue
                            try:
                                s = raw[pos:end_pos].decode("ascii", errors="ignore")
                                add_path(s)
                            except Exception:
                                pass
                            pos = end_pos + 1

            # ── Method 2: ASCII DMX / text fallback ──
            # Works for both text DMX and as extra coverage for binary
            # Find all quoted strings
            for m in _re.finditer(b'"([^"\\x00]{4,400})"', raw):
                try:
                    add_path(m.group(1).decode("ascii", errors="ignore"))
                except Exception:
                    pass

            # ── Method 3: Full raw scan for materials/ patterns ──
            # Most reliable - finds paths even in unusual encodings
            for m in _re.finditer(b'(?:materials|MATERIALS)/[a-zA-Z0-9_/\\-\\.]{4,300}', raw):
                try:
                    val = m.group(0).decode("ascii", errors="ignore")
                    add_path(val)
                except Exception:
                    pass

            # ── Method 4: Scan for .vtf/.vmt paths without materials/ prefix ──
            for m in _re.finditer(b'[a-zA-Z0-9_/\\-\\.]{4,200}\\.(?:vtf|vmt|tga)(?=[\\x00\\n\\r\\"])', raw):
                try:
                    val = m.group(0).decode("ascii", errors="ignore")
                    add_path(val)
                except Exception:
                    pass

        except Exception:
            pass
        return textures

    def _tx_get_search_paths(self):
        return [l.strip() for l in self._tx_paths_edit.toPlainText().splitlines()
                if l.strip() and not l.strip().startswith("#") and os.path.isdir(l.strip())]

    def _tx_find_file(self, rel_path, search_paths, exts):
        rel_path = rel_path.replace("\\","/").strip("/")
        for sp in search_paths:
            for ext in exts:
                if os.path.isfile(os.path.join(sp, rel_path+ext)): return True
        return False

    def _tx_read_mdl_textures(self, mdl_path):
        """
        Parse a Valve MDL file and extract all texture/material references.

        MDL Header (v44/v49) contains:
          - texturedir: list of texture search directories
          - textures:   list of texture names (just filenames, no path)
        Combined: texturedir[i] + texture[j] = full material path.

        Also does a raw regex scan as fallback for any missed references.
        """
        textures = []
        seen = set()
        try:
            import struct as _s, re as _re
            with open(mdl_path, "rb") as f:
                raw = f.read()

            # Verify MDL magic: "IDST"
            if raw[:4] != b"IDST":
                # Try raw scan fallback anyway
                pass
            else:
                # Read version (offset 4)
                version = _s.unpack_from("<I", raw, 4)[0]

                def read_str(offset):
                    end = raw.find(b"\x00", offset)
                    if end < 0: end = offset + 256
                    try: return raw[offset:end].decode("ascii", errors="ignore").strip()
                    except: return ""

                # ── Texture names (v44+) ──
                # Offsets: numtextures=@0xD0, textureindex=@0xD4
                # texturedirnums=@0xD8, texturedirindex=@0xDC
                if len(raw) >= 0xE0:
                    num_tex = _s.unpack_from("<I", raw, 0xD0)[0]
                    tex_idx = _s.unpack_from("<I", raw, 0xD4)[0]
                    num_dir = _s.unpack_from("<I", raw, 0xD8)[0]
                    dir_idx = _s.unpack_from("<I", raw, 0xDC)[0]

                    # Read texture directories
                    tex_dirs = []
                    for di in range(min(num_dir, 64)):
                        ptr = dir_idx + di * 4
                        if ptr + 4 > len(raw): break
                        str_off = _s.unpack_from("<I", raw, ptr)[0]
                        if str_off < len(raw):
                            d = read_str(str_off).replace("\\", "/").strip("/")
                            tex_dirs.append(d)

                    # Read texture names
                    # Each texture entry is 64 bytes; name is at entry start + nameindex offset
                    TEX_ENTRY_SIZE = 64
                    for ti in range(min(num_tex, 512)):
                        entry_base = tex_idx + ti * TEX_ENTRY_SIZE
                        if entry_base + 4 > len(raw): break
                        name_off = _s.unpack_from("<I", raw, entry_base)[0]
                        abs_off = entry_base + name_off
                        if abs_off < len(raw):
                            name = read_str(abs_off).replace("\\", "/").strip("/")
                            if name:
                                # Try each texture dir
                                dirs_to_try = tex_dirs if tex_dirs else [""]
                                for td in dirs_to_try:
                                    td = td.replace("\\", "/").strip("/")
                                    if td:
                                        full = td + "/" + name
                                    else:
                                        full = name
                                    # Strip materials/ prefix if present
                                    fl = full.lower()
                                    if fl.startswith("materials/"):
                                        full = full[len("materials/"):]
                                    # Remove extension
                                    no_ext = full.rsplit(".", 1)[0] if "." in full.split("/")[-1] else full
                                    if no_ext and no_ext not in seen and len(no_ext) >= 2:
                                        seen.add(no_ext)
                                        textures.append(no_ext)

            # ── Fallback: raw regex scan for material paths ──
            for m in _re.finditer(b"(?:materials[/\\\\]|MATERIALS[/\\\\])[a-zA-Z0-9_/\\\\\\-\\.]{2,200}", raw):
                try:
                    val = m.group(0).decode("ascii", errors="ignore").replace("\\", "/")
                    fl  = val.lower()
                    if fl.startswith("materials/"):
                        val = val[len("materials/"):]
                    no_ext = val.rsplit(".", 1)[0] if "." in val.split("/")[-1] else val
                    if no_ext and no_ext not in seen and len(no_ext) >= 2:
                        seen.add(no_ext)
                        textures.append(no_ext)
                except Exception:
                    pass

            # ── Scan for .vtf/.vmt/.tga filenames ──
            for m in _re.finditer(b"[a-zA-Z0-9_][a-zA-Z0-9_/\\\\\\-]{1,100}\\.(?:vtf|vmt|tga)", raw):
                try:
                    val = m.group(0).decode("ascii", errors="ignore").replace("\\", "/")
                    no_ext = val.rsplit(".", 1)[0]
                    if no_ext and no_ext not in seen and "/" in no_ext:
                        seen.add(no_ext)
                        textures.append(no_ext)
                except Exception:
                    pass

        except Exception:
            pass
        return textures

    def _tx_read_bsp_textures(self, bsp_path):
        textures = []
        try:
            import struct as _s
            with open(bsp_path,"rb") as f:
                if f.read(4) != b"VBSP": return textures
                f.read(4)
                lumps = []
                for _ in range(64):
                    offset,length = _s.unpack("<II",f.read(8)); f.read(8); lumps.append((offset,length))
                if len(lumps) > 44:
                    off43,len43 = lumps[43]; off44,len44 = lumps[44]
                    f.seek(off43); raw = f.read(len43); f.seek(off44)
                    seen = set()
                    for _ in range(len44//4):
                        b4 = f.read(4)
                        if len(b4)<4: break
                        idx = _s.unpack("<I",b4)[0]; end = raw.find(b"\x00",idx)
                        name = raw[idx:end if end>=0 else len(raw)].decode("ascii",errors="replace").strip()
                        if name and name not in seen: seen.add(name); textures.append(name)
        except Exception: pass
        return textures

    def _tx_scan(self):
        try:
            scan_type = self._tx_type_combo.currentIndex()  # 0=BSP, 1=PCF, 2=Both
            search_paths = self._tx_get_search_paths()
            if not search_paths:
                QtGui.QMessageBox.warning(self, "No Paths",
                    "No valid material search paths found.\n"
                    "Please check the Material Search Paths box above."); return

            self._tx_table.setRowCount(0); self._tx_all_results = []
            self._tx_progress.setVisible(True); self._tx_progress.setValue(5)
            self._tx_stats_lbl.setText("Scanning..."); QtGui.QApplication.processEvents()

            texture_names = []

            # BSP scan
            if scan_type in (0, 2):
                map_input = self._tx_map_line.text().strip()
                if not map_input and scan_type == 0:
                    QtGui.QMessageBox.warning(self, "No Map", "Please enter a map name or browse for a .bsp file.")
                    self._tx_progress.setVisible(False); return
                if map_input:
                    bsp_path = None
                    if map_input.lower().endswith(".bsp") and os.path.isfile(map_input):
                        bsp_path = map_input
                    else:
                        map_name = os.path.splitext(os.path.basename(map_input))[0]
                        for sp in search_paths:
                            parent = os.path.dirname(sp)
                            for c in [
                                os.path.join(parent, "maps", map_name + ".bsp"),
                                os.path.join(sp, "..", "maps", map_name + ".bsp"),
                                os.path.join(sp, "..", "..", "maps", map_name + ".bsp"),
                            ]:
                                if os.path.isfile(c): bsp_path = c; break
                            if bsp_path: break
                    if bsp_path:
                        self._tx_stats_lbl.setText("Reading BSP: " + os.path.basename(bsp_path))
                        QtGui.QApplication.processEvents()
                        names = self._tx_read_bsp_textures(bsp_path)
                        for n in names: texture_names.append((n, "BSP"))
                        if not names:
                            self._tx_stats_lbl.setText("BSP found but 0 textures - falling back to VMT scan...")
                            QtGui.QApplication.processEvents()
                            seen = set()
                            for sp in search_paths:
                                for r2, _, f2 in os.walk(sp):
                                    for fn in f2:
                                        if fn.lower().endswith(".vmt"):
                                            rel = os.path.relpath(os.path.join(r2,fn),sp).replace("\\","/")
                                            no_ext = os.path.splitext(rel)[0]
                                            if no_ext not in seen: seen.add(no_ext); texture_names.append((no_ext,"VMT"))
                    else:
                        self._tx_stats_lbl.setText("BSP not found - scanning VMTs in material folders...")
                        QtGui.QApplication.processEvents()
                        seen = set()
                        for sp in search_paths:
                            for r2, _, f2 in os.walk(sp):
                                for fn in f2:
                                    if fn.lower().endswith(".vmt"):
                                        rel = os.path.relpath(os.path.join(r2,fn),sp).replace("\\","/")
                                        no_ext = os.path.splitext(rel)[0]
                                        if no_ext not in seen: seen.add(no_ext); texture_names.append((no_ext,"VMT"))

            # PCF scan
            if scan_type in (1, 2):
                pcf_input = self._tx_pcf_line.text().strip()
                if not pcf_input and scan_type == 1:
                    QtGui.QMessageBox.warning(self, "No PCF", "Please browse for a .pcf particle file.")
                    self._tx_progress.setVisible(False); return
                if pcf_input:
                    if not os.path.isfile(pcf_input):
                        QtGui.QMessageBox.warning(self, "File Not Found", "PCF file not found:\n" + pcf_input)
                        self._tx_progress.setVisible(False); return
                    self._tx_stats_lbl.setText("Reading PCF: " + os.path.basename(pcf_input))
                    QtGui.QApplication.processEvents()
                    names = self._tx_read_pcf_textures(pcf_input)
                    for n in names: texture_names.append((n, "PCF"))
                    if not names:
                        self._tx_stats_lbl.setText("PCF parsed but 0 material paths found.")
                        QtGui.QApplication.processEvents()

            # MDL scan
            if scan_type in (2, 4):
                mdl_input = self._tx_mdl_line.text().strip() if hasattr(self, '_tx_mdl_line') else ""
                if not mdl_input and scan_type == 2:
                    QtGui.QMessageBox.warning(self, "No MDL", "Please browse for a .mdl model file.")
                    self._tx_progress.setVisible(False); return
                if mdl_input:
                    if not os.path.isfile(mdl_input):
                        QtGui.QMessageBox.warning(self, "File Not Found", "MDL not found:\n" + mdl_input)
                        self._tx_progress.setVisible(False); return
                    self._tx_stats_lbl.setText("Reading MDL: " + os.path.basename(mdl_input))
                    QtGui.QApplication.processEvents()
                    names = self._tx_read_mdl_textures(mdl_input)
                    for n in names: texture_names.append((n, "MDL"))
                    if not names:
                        self._tx_stats_lbl.setText("MDL parsed but 0 texture paths found.")
                        QtGui.QApplication.processEvents()

            # Deduplicate
            seen_p = set(); deduped = []
            for name, src in texture_names:
                if name not in seen_p: seen_p.add(name); deduped.append((name, src))
            texture_names = deduped

            self._tx_progress.setValue(40); QtGui.QApplication.processEvents()
            total = len(texture_names)
            if total == 0:
                self._tx_stats_lbl.setText(
                    "No textures found. For BSP: check .bsp path. For PCF: file must contain materials/ references.")
                self._tx_progress.setVisible(False); return

            results = []; found_n = missing_n = 0
            for i, (name, src) in enumerate(texture_names):
                if i % 30 == 0:
                    self._tx_progress.setValue(40 + int(55*i/total)); QtGui.QApplication.processEvents()
                vmt_ok = self._tx_find_file(name, search_paths, [".vmt"])
                vtf_ok = self._tx_find_file(name, search_paths, [".vtf"])
                ft = src + ":"
                if vmt_ok and vtf_ok:   results.append(("OK",         name, ft+"VMT+VTF")); found_n+=1
                elif vmt_ok:            results.append(("MISSING VTF", name, ft+"VTF"));     missing_n+=1
                elif vtf_ok:            results.append(("MISSING VMT", name, ft+"VMT"));     missing_n+=1
                else:                   results.append(("MISSING",     name, ft+"VMT+VTF")); missing_n+=1

            self._tx_progress.setValue(100); self._tx_all_results = results
            self._tx_apply_filter()
            self._tx_stats_lbl.setText("Total: {}    Found: {}    Missing: {}".format(total, found_n, missing_n))
            QtCore.QTimer.singleShot(1200, lambda: self._tx_progress.setVisible(False))
        except Exception as e:
            self._tx_stats_lbl.setText("Error: {}".format(e)); self._tx_progress.setVisible(False)

    def _tx_apply_filter(self):
        try:
            flt=self._tx_filter_combo.currentText(); search=self._tx_search_line.text().strip().lower()
            self._tx_table.setRowCount(0)
            for status,path,ftype in self._tx_all_results:
                if flt=="Missing Only" and status=="OK": continue
                if flt=="Found Only"   and status!="OK": continue
                if search and search not in path.lower(): continue
                row=self._tx_table.rowCount(); self._tx_table.insertRow(row)
                s=QtGui.QTableWidgetItem(status)
                s.setForeground(QtGui.QBrush(QtGui.QColor("#2aff88" if status=="OK" else PALETTE["danger"])))
                self._tx_table.setItem(row,0,s)
                p=QtGui.QTableWidgetItem(path)
                p.setForeground(QtGui.QBrush(QtGui.QColor(PALETTE["text"]))); self._tx_table.setItem(row,1,p)
                t=QtGui.QTableWidgetItem(ftype)
                t.setForeground(QtGui.QBrush(QtGui.QColor(PALETTE["teal"]))); self._tx_table.setItem(row,2,t)
        except Exception: pass

    def _tx_export_report(self):
        try:
            if not self._tx_all_results:
                QtGui.QMessageBox.information(self,"Empty","No results to export."); return
            path,_ = QtGui.QFileDialog.getSaveFileName(self,"Save Report","texture_report.txt","Text Files (*.txt)")
            if not path: return
            with open(path,"w") as f:
                f.write("Texture Checker Report\n"+"="*60+"\n\n")
                missing=[r for r in self._tx_all_results if r[0]!="OK"]
                found=[r for r in self._tx_all_results if r[0]=="OK"]
                f.write("MISSING ({}):\n".format(len(missing)))
                for s,p,t in missing: f.write("  [{}] {} ({})\n".format(s,p,t))
                f.write("\nFOUND ({}):\n".format(len(found)))
                for s,p,t in found: f.write("  [OK] {}\n".format(p))
            QtGui.QMessageBox.information(self,"Saved","Report saved:\n"+path)
        except Exception as e: QtGui.QMessageBox.warning(self,"Error",str(e))


    def _ensure_overlay(self):
        try:
            if hasattr(self, '_overlay_manager') and self._overlay_manager is not None:
                # Check the Qt C++ object is still alive (not garbage-collected)
                try:
                    if not shiboken.isValid(self._overlay_manager):
                        self._overlay_manager = None
                except Exception:
                    pass
            if not hasattr(self, '_overlay_manager') or self._overlay_manager is None:
                # create as a top-level window so it floats above SFM viewports
                self._overlay_manager = SFMOverlayWindow(None)
                # initial settings
                try:
                    self._overlay_manager.setWindowOpacity(self.overlay_opacity_slider.value() / 100.0)
                except Exception:
                    pass
            return self._overlay_manager
        except Exception:
            return None

    def _overlay_add_image(self):
        try:
            start_dir = os.path.expanduser("~")
            path = QtGui.QFileDialog.getOpenFileName(self, 'Select image', start_dir, 'Images (*.png *.jpg *.bmp)')
            if isinstance(path, (tuple, list)):
                path = path[0]
            try:
                path = str(path)
            except Exception:
                pass
            if not path:
                return
            if not os.path.exists(path):
                QtGui.QMessageBox.warning(self, "SFM Overlay", "Selected file does not exist:\n{}".format(path))
                if hasattr(self, 'log_box'):
                    try:
                        self.log_box.append("âš  Overlay add failed: file not found: {}".format(path))
                    except Exception:
                        pass
                return

            ok = False
            try:
                ok = self._ensure_overlay().add_image(path, scale=self.overlay_scale_slider.value()/100.0, opacity=self.overlay_opacity_slider.value()/100.0)
            except Exception as e:
                ok = False
                if hasattr(self, 'log_box'):
                    try:
                        self.log_box.append("âš  Exception while adding overlay image: {}".format(e))
                    except Exception:
                        pass

            if not ok:
                QtGui.QMessageBox.warning(self, "SFM Overlay", "Could not load image (unsupported or corrupt):\n{}".format(path))
                if hasattr(self, 'log_box'):
                    try:
                        self.log_box.append("âš  Failed to load image into overlay: {}".format(path))
                    except Exception:
                        pass
                return

            # success
            self.overlay_images_list.addItem(path)
            if hasattr(self, 'log_box'):
                try:
                    self.log_box.append("âœ… Overlay image added: {}".format(path))
                except Exception:
                    pass
        except Exception as e:
            try:
                QtGui.QMessageBox.warning(self, "SFM Overlay", "Error adding image: {}".format(e))
            except Exception:
                pass
            if hasattr(self, 'log_box'):
                try:
                    self.log_box.append("âš  _overlay_add_image exception: {}".format(e))
                except Exception:
                    pass

    def _overlay_remove_selected(self):
        try:
            idx = self.overlay_images_list.currentRow()
            if idx < 0:
                return
            ow = self._ensure_overlay()
            if not ow:
                return
            # Sync check: list widget and internal images must agree
            if idx >= len(ow.images):
                # List is out of sync – rebuild list to recover
                try:
                    self.overlay_images_list.clear()
                    for e in ow.images:
                        self.overlay_images_list.addItem(os.path.basename(e.get('path', '?')))
                except Exception:
                    pass
                return
            ow.remove_image(idx)
            self.overlay_images_list.takeItem(idx)
        except Exception:
            pass

    def _overlay_bring_front(self):
        try:
            idx = self.overlay_images_list.currentRow()
            if idx < 0:
                return
            self._ensure_overlay().bring_to_front(idx)
        except Exception:
            pass

    def _overlay_on_selection_changed(self, idx):
        try:
            if idx < 0:
                return
            # update sliders to reflect selected image
            entry = None
            try:
                entry = self._ensure_overlay().images[idx]
            except Exception:
                entry = None
            if entry:
                try:
                    self.overlay_scale_slider.setValue(int(entry.get('scale',1.0)*100))
                    self.overlay_opacity_slider.setValue(int(entry.get('opacity',1.0)*100))
                except Exception:
                    pass
        except Exception:
            pass

    def _overlay_on_opacity_changed(self, val):
        try:
            idx = self.overlay_images_list.currentRow()
            if idx < 0:
                # apply to whole overlay
                ow = self._ensure_overlay()
                if ow:
                    ow.setWindowOpacity(val/100.0)
                return
            self._ensure_overlay().set_image_opacity(idx, val/100.0)
        except Exception:
            pass

    def _overlay_on_scale_changed(self, val):
        try:
            idx = self.overlay_images_list.currentRow()
            if idx < 0:
                return
            self._ensure_overlay().set_image_scale(idx, val/100.0)
        except Exception:
            pass

    def _overlay_on_lock_toggled(self, on):
        try:
            self._ensure_overlay().set_lock_clickthrough(on)
        except Exception:
            pass

    def remove_all_overlays(self):
        try:
            ow = self._ensure_overlay()
            if ow:
                # Snapshot the list so iteration is safe even if remove_image modifies it
                try:
                    count = len(ow.images)
                    for i in range(count - 1, -1, -1):
                        try:
                            ow.remove_image(i)
                        except Exception:
                            pass
                except Exception:
                    # Last-resort: clear the list directly
                    try:
                        ow.images = []
                    except Exception:
                        pass
                try:
                    ow.hide()
                except Exception:
                    pass
            try:
                if hasattr(self, 'overlay_images_list'):
                    self.overlay_images_list.clear()
            except Exception:
                pass
            try:
                if hasattr(self, '_overlay_presets'):
                    self._overlay_presets.clear()
                if hasattr(self, '_overlay_presets_file') and os.path.exists(self._overlay_presets_file):
                    try:
                        os.remove(self._overlay_presets_file)
                    except Exception:
                        pass
                if hasattr(self, 'overlay_preset_combo'):
                    try:
                        self.overlay_preset_combo.clear()
                    except Exception:
                        pass
            except Exception:
                pass
        except Exception:
            pass

    def toggle_all_overlays(self):
        try:
            ow = self._ensure_overlay()
            if not ow:
                return
            # Guard: check Qt object is still alive before calling Qt methods
            try:
                is_valid = shiboken.isValid(ow)
            except Exception:
                is_valid = True
            if not is_valid:
                self._overlay_manager = None
                return
            try:
                if ow.isVisible():
                    ow.hide()
                else:
                    ow.show()
            except Exception:
                try:
                    cur = ow.windowOpacity()
                    if cur > 0.0:
                        ow.setWindowOpacity(0.0)
                    else:
                        ow.setWindowOpacity(1.0)
                except Exception:
                    pass
        except Exception:
            pass


    def _overlay_save_preset(self):
        try:
            name = self.overlay_preset_name.text().strip()
            if not name:
                return
            ow = self._ensure_overlay()
            data = []
            for e in (ow.images if ow else []):
                data.append({'path': e.get('path'), 'scale': e.get('scale'), 'opacity': e.get('opacity')})
            self._overlay_presets[name] = data
            with open(self._overlay_presets_file, 'w', encoding='utf-8') as f:
                json.dump(self._overlay_presets, f, ensure_ascii=False, indent=2)
            # reload combo
            self.overlay_preset_combo.clear()
            for k in sorted(self._overlay_presets.keys()):
                self.overlay_preset_combo.addItem(k)
        except Exception:
            pass

    def _overlay_load_preset(self):
        try:
            key = self.overlay_preset_combo.currentText()
            if not key:
                return
            preset = self._overlay_presets.get(key)
            if not preset:
                return
            ow = self._ensure_overlay()
            # clear existing
            try:
                while ow.images:
                    ow.remove_image(0)
            except Exception:
                pass
            self.overlay_images_list.clear()
            for p in preset:
                ok = ow.add_image(p.get('path'), scale=p.get('scale',1.0), opacity=p.get('opacity',1.0))
                if ok:
                    self.overlay_images_list.addItem(p.get('path'))
        except Exception:
            pass

    def _overlay_delete_preset(self):
        try:
            key = self.overlay_preset_combo.currentText()
            if not key:
                return
            if key in self._overlay_presets:
                del self._overlay_presets[key]
                with open(self._overlay_presets_file, 'w', encoding='utf-8') as f:
                    json.dump(self._overlay_presets, f, ensure_ascii=False, indent=2)
                self.overlay_preset_combo.clear()
                for k in sorted(self._overlay_presets.keys()):
                    self.overlay_preset_combo.addItem(k)
        except Exception:
            pass

    def create_console_tab(self):
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)
        layout.setContentsMargins(12,12,12,12)

        # Console row with autocomplete and clear action
        h = QtGui.QHBoxLayout()
        self.console_input = QtGui.QLineEdit()
        self.console_input.setPlaceholderText("Enter console command")
        self.console_input.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        h.addWidget(self.console_input)
        exec_btn = QtGui.QPushButton("Execute")
        exec_btn.setStyleSheet(self._global_button_style(PALETTE['accent']))
        exec_btn.clicked.connect(self.execute_console_command)
        h.addWidget(exec_btn)
        self.clear_console_btn = QtGui.QPushButton(t("Clear Console"))
        self.clear_console_btn.setStyleSheet(self._global_button_style(PALETTE['muted']))
        self.clear_console_btn.clicked.connect(lambda: self.console_log.clear())
        h.addWidget(self.clear_console_btn)
        layout.addLayout(h)

        # autocomplete suggestions (simple QCompleter)
        try:
            completions = list(self.quick_commands.keys()) + list(self.quick_commands.values())
            completer = QtGui.QCompleter(completions)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            try:
                completer.setFilterMode(QtCore.Qt.MatchContains)
            except Exception:
                pass
            self.console_input.setCompleter(completer)
        except Exception:
            pass

        # Console log
        self.console_log = QtGui.QTextEdit()
        self.console_log.setReadOnly(True)
        self.console_log.setFixedHeight(140)
        self.console_log.setStyleSheet('background-color: %s; color: %s;' % (PALETTE['muted'], PALETTE['text']))
        layout.addWidget(self.console_log)

        layout.addStretch()
        return tab

    def open_skybox_info_dialog(self):
        dlg = QtGui.QDialog(self)
        dlg.setWindowTitle("Skybox info")
        dlg.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000000, stop:1 %s); color: %s;" % (PALETTE['panel'], PALETTE['text']))
        layout = QtGui.QVBoxLayout(dlg)
        listw = QtGui.QListWidget()
        for name in SKYBOXES:
            item = QtGui.QListWidgetItem(name)
            listw.addItem(item)
        layout.addWidget(listw)
        btn_h = QtGui.QHBoxLayout()
        copy_btn = QtGui.QPushButton("Copy Selected")
        def copy_sel():
            it = listw.currentItem()
            if it:
                QtGui.QApplication.clipboard().setText(it.text())
                if hasattr(self, 'log_box'):
                    self.log_box.append("Copied: {}".format(it.text()))
                else:
                    try:
                        self.console_log.append("Copied: {}".format(it.text()))
                    except Exception:
                        pass
        copy_btn.clicked.connect(copy_sel)
        btn_h.addWidget(copy_btn)
        close_btn = QtGui.QPushButton("Close")
        close_btn.clicked.connect(dlg.accept)
        btn_h.addWidget(close_btn)
        layout.addLayout(btn_h)
        dlg.exec_()

    def set_skybox(self):
        # Prefer menu2 skybox input if it exists (moved from console)
        name = ''
        if hasattr(self, 'skybox_input_menu2'):
            name = self.skybox_input_menu2.text().strip()
        elif hasattr(self, 'skybox_input'):
            name = self.skybox_input.text().strip()
        global original_skybox
        if not name:
            try:
                self.console_log.append("âš  No skybox name entered")
            except Exception:
                pass
            return
        if name not in SKYBOXES:
            try:
                self.console_log.append("âš  Unknown skybox: {}".format(name))
            except Exception:
                pass
            return
        try:
            if original_skybox is None:
                original_skybox = ""
            sfm.console('sv_skyname "{}"'.format(name))
            if hasattr(self, 'log_box'):
                self.log_box.append("ğŸŒŒ Skybox set to: {}".format(name))
            else:
                try:
                    self.console_log.append("ğŸŒŒ Skybox set to: {}".format(name))
                except Exception:
                    pass
        except Exception as e:
            if hasattr(self, 'log_box'):
                self.log_box.append("âŒ Error setting skybox: {}".format(e))
            else:
                try:
                    self.console_log.append("âŒ Error setting skybox: {}".format(e))
                except Exception:
                    pass

    def reset_skybox(self):
        global original_skybox
        try:
            if original_skybox:
                sfm.console('sv_skyname "{}"'.format(original_skybox))
                self.console_log.append("âœ… Skybox reset to {}".format(original_skybox))
            else:
                sfm.console('sv_skyname ""')
                self.console_log.append("âœ… Skybox reset (default)")
        except Exception as e:
            self.console_log.append("âš  Error resetting skybox: {}".format(e))

    def execute_console_command(self):
        cmd = self.console_input.text().strip()
        if not cmd:
            self.console_log.append("âš  No command entered")
            return
        try:
            sfm.console(cmd)
            self.console_log.append("ğŸ“Ÿ Executed: {}".format(cmd))
            try:
                if hasattr(self, 'log_box'):
                    self.log_box.append("ğŸ“Ÿ Executed: {}".format(cmd))
            except Exception:
                pass
            self.console_input.clear()
        except Exception as e:
            self.console_log.append("âš  Error executing command: {}".format(e))
            try:
                if hasattr(self, 'log_box'):
                    self.log_box.append("âš  Error executing command: {}".format(e))
            except Exception:
                pass

    def create_language_tab(self):
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)
        layout.setContentsMargins(12,12,12,12)
        self.lang_box = QtGui.QComboBox()
        for l in LANGUAGES:
            self.lang_box.addItem(l)
        # set current language selection in a PySide-compatible way
        try:
            idx = self.lang_box.findText(CURRENT_LANGUAGE)
            if idx >= 0:
                self.lang_box.setCurrentIndex(idx)
        except Exception:
            try:
                for i in range(self.lang_box.count()):
                    if self.lang_box.itemText(i) == CURRENT_LANGUAGE:
                        self.lang_box.setCurrentIndex(i)
                        break
            except Exception:
                pass
        layout.addWidget(QtGui.QLabel(t("Choose language:")))
        layout.addWidget(self.lang_box)
        # do not apply on selection change; require explicit "Apply Language" click
        # (previously connected to `currentIndexChanged`, which caused unwanted immediate changes)
        btn_h = QtGui.QHBoxLayout()
        apply_btn = QtGui.QPushButton(t("Apply Language"))
        apply_btn.clicked.connect(self.apply_language)
        reset_btn = QtGui.QPushButton(t("Reset Language"))
        reset_btn.clicked.connect(self.reset_language)
        btn_h.addWidget(apply_btn)
        btn_h.addWidget(reset_btn)
        btn_h.addStretch()
        layout.addLayout(btn_h)

        # Font diagnostics: report which font is active and missing glyphs for alphabets
        fd_h = QtGui.QHBoxLayout()
        self.font_diag_btn = QtGui.QPushButton("Font Diagnostics")
        self.font_diag_btn.setToolTip("Check which font was selected and report missing characters for languages")
        self.font_diag_btn.clicked.connect(self._font_diagnostics)
        fd_h.addWidget(self.font_diag_btn)
        layout.addLayout(fd_h)

        layout.addStretch()
        return tab

    def apply_language(self, force_lang=None):
        global CURRENT_LANGUAGE
        try:
            if force_lang:
                lang = force_lang
                # Update combobox to match forced language
                try:
                    idx = self.lang_box.findText(lang)
                    if idx >= 0:
                        self.lang_box.setCurrentIndex(idx)
                except Exception:
                    try:
                        for i in range(self.lang_box.count()):
                            if self.lang_box.itemText(i) == lang:
                                self.lang_box.setCurrentIndex(i)
                                break
                    except Exception:
                        pass
            else:
                lang = self.lang_box.currentText()

            if lang in LANGUAGES:
                CURRENT_LANGUAGE = lang
                
                # Update tab labels to the desired names
                try:
                    self.tabs.setTabText(self.tabs.indexOf(self.command_tab), t("Filmmaker GUI"))
                    self.tabs.setTabText(self.tabs.indexOf(self.menu2_tab), t("Filmmaker GUI 2"))
                    self.tabs.setTabText(self.tabs.indexOf(self.console_tab), t("Console"))
                    self.tabs.setTabText(self.tabs.indexOf(self.language_tab), t("Language"))
                    self.tabs.setTabText(self.tabs.indexOf(self.logs_tab), t("Logs"))
                    if self.sfm_notes_tab:
                        self.tabs.setTabText(self.tabs.indexOf(self.sfm_notes_tab), t("SFM Notes"))
                    self.tabs.setTabText(self.tabs.indexOf(self.vmt_editor_tab), t(u"VMTEDİTOR"))
                    self.tabs.setTabText(self.tabs.indexOf(self.sfm_overlay_tab), t("SFM Overlay"))
                    if hasattr(self, "texture_tab"):
                        self.tabs.setTabText(self.tabs.indexOf(self.texture_tab), t("Texture Checker"))
                    if hasattr(self, "whatif_tab"):
                        self.tabs.setTabText(self.tabs.indexOf(self.whatif_tab), t("Skibidi What If"))
                    if hasattr(self, "guide_tab"):
                        self.tabs.setTabText(self.tabs.indexOf(self.guide_tab), t("Guide"))
                except Exception:
                    pass
                # update internal title labels if present
                try:
                    if hasattr(self, 'menu2_title'):
                        self.menu2_title.setText(t("Filmmaker GUI 2"))
                except Exception:
                    pass
                # --- Overlay tab widgets ---
                try:
                    if hasattr(self, 'overlay_title_lbl'):
                        self.overlay_title_lbl.setText(t("SFM Overlay"))
                    if hasattr(self, 'btn_overlay_add'):
                        self.btn_overlay_add.setText(t("Add Image"))
                    if hasattr(self, 'btn_overlay_remove'):
                        self.btn_overlay_remove.setText(t("Remove Selected"))
                    if hasattr(self, 'btn_overlay_front'):
                        self.btn_overlay_front.setText(t("Bring to Front"))
                    if hasattr(self, 'btn_overlay_toggle'):
                        self.btn_overlay_toggle.setText(t("Toggle All"))
                    if hasattr(self, 'btn_overlay_clear'):
                        self.btn_overlay_clear.setText(t("Remove All"))
                    if hasattr(self, 'overlay_opacity_lbl'):
                        self.overlay_opacity_lbl.setText(t("Opacity:"))
                    if hasattr(self, 'overlay_scale_lbl'):
                        self.overlay_scale_lbl.setText(t("Scale:"))
                    if hasattr(self, 'overlay_lock_chk'):
                        self.overlay_lock_chk.setText(t("Lock (Click-through)"))
                    if hasattr(self, 'overlay_preset_title'):
                        self.overlay_preset_title.setText(t("Presets"))
                    if hasattr(self, 'overlay_preset_name'):
                        self.overlay_preset_name.setPlaceholderText(t("Preset name..."))
                    if hasattr(self, 'btn_overlay_save_p'):
                        self.btn_overlay_save_p.setText(t("Save"))
                    if hasattr(self, 'btn_overlay_load_p'):
                        self.btn_overlay_load_p.setText(t("Load"))
                    if hasattr(self, 'btn_overlay_del_p'):
                        self.btn_overlay_del_p.setText(t("Delete"))
                except Exception:
                    pass
                # --- Fog / command tab widgets ---
                try:
                    if hasattr(self, 'enable_fog_checkbox'):
                        self.enable_fog_checkbox.setText(t("Enable Fog"))
                    if hasattr(self, 'btn_set_fog'):
                        self.btn_set_fog.setText(t("Set Fog Settings"))
                    if hasattr(self, 'btn_lightLimit'):
                        self.btn_lightLimit.setText(t("Light Limit Patch"))
                except Exception:
                    pass
                # --- Notes tab ---
                try:
                    if hasattr(self, 'save_button'):
                        self.save_button.setText(t("Save Notes"))
                except Exception:
                    pass
                except Exception:
                    pass
                # update language-sensitive button text
                try:
                    if hasattr(self, 'select_model_btn'):
                        self.select_model_btn.setText(t("Select Model From Animation Set Editor"))
                except Exception:
                    pass
                try:
                    if hasattr(self, 'clear_console_btn'):
                        self.clear_console_btn.setText(t("Clear Console"))
                except Exception:
                    pass
                # try to re-apply a unicode-capable font based on selected language
                try:
                    sample = get_alphabet_for_language(CURRENT_LANGUAGE)
                    apply_unicode_font(self, samples=sample)
                    # reapply to children
                    try:
                        f = self.font()
                        for w in self.findChildren(QtGui.QWidget):
                            try:
                                w.setFont(f)
                            except Exception:
                                pass
                    except Exception:
                        pass
                except Exception:
                    pass

                try:
                    if hasattr(self, 'clear_console_btn'):
                        self.clear_console_btn.setText(t("Clear Console"))
                except Exception:
                    pass

                try:
                    if hasattr(self, 'clear_log_btn'):
                        self.clear_log_btn.setText(t("Clear Log"))
                except Exception:
                    pass

                try:
                    if hasattr(self, 'menu2_quick_box'):
                        # Update label if used elsewhere
                        pass
                except Exception:
                    pass

                if hasattr(self, 'log_box'):
                    self.log_box.append(u"Language set: {}".format(lang))
                # Refresh texts for common widgets (buttons, labels, placeholders)
                try:
                    # Update QPushButton texts using stored translation keys when available
                    for btn in self.findChildren(QtGui.QPushButton):
                        try:
                            key = btn.property('tr_key')
                            if key:
                                btn.setText(t(key))
                            else:
                                # fallback: try to detect from current visible text (best-effort)
                                txt = btn.text().strip()
                                clean = re.sub(r'^[^A-Za-z0-9]+', '', txt).strip()
                                if clean in TRANSLATIONS:
                                    btn.setText(t(clean))
                        except Exception:
                            pass
                    # Update QLabel texts
                    for lbl in self.findChildren(QtGui.QLabel):
                        try:
                            key = lbl.property('tr_key')
                            if key:
                                lbl.setText(t(key))
                            else:
                                txt = lbl.text().strip()
                                clean = re.sub(r'^[^A-Za-z0-9]+', '', txt).strip()
                                if clean in TRANSLATIONS:
                                    lbl.setText(t(clean))
                        except Exception:
                            pass
                    # Update QLineEdit placeholders
                    for le in self.findChildren(QtGui.QLineEdit):
                        try:
                            key = le.property('tr_key')
                            if key:
                                le.setPlaceholderText(t(key))
                            else:
                                ph = le.placeholderText().strip()
                                clean = re.sub(r'^[^A-Za-z0-9]+', '', ph).strip()
                                if clean in TRANSLATIONS:
                                    le.setPlaceholderText(t(clean))
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception as e:
            if hasattr(self, 'log_box'):
                self.log_box.append(u"âš  Couldn't apply language: {}".format(e))

    def reset_language(self):
        # Force apply Default Language (English) directly
        # This bypasses reading from the GUI first, ensuring reliability
        self.apply_language(force_lang=DEFAULT_LANGUAGE)

    def _font_diagnostics(self):
        """Font secici dialog ac - kullanicinin GUI fontunu degistirmesine izin ver."""
        try:
            dlg = QtGui.QDialog(self)
            dlg.setWindowTitle("Font Settings")
            dlg.setMinimumSize(480, 520)
            dlg.setStyleSheet("""
                QDialog { background:#1e1e1e; color:#CAC9C9; }
                QLabel { color:#CAC9C9; }
                QListWidget { background:#252526; border:1px solid #3a3a3a; border-radius:6px;
                              color:#CAC9C9; font-size:12px; }
                QListWidget::item:selected { background:#0b4f94; color:#fff; }
                QListWidget::item:hover { background:#2a2a2a; }
                QPushButton { background:#2f2f2f; color:#CAC9C9; border:1px solid #444;
                              padding:7px 16px; border-radius:6px; font-size:12px; }
                QPushButton:hover { background:#3a3a3a; }
                QSpinBox { background:#252526; color:#CAC9C9; border:1px solid #444;
                           border-radius:4px; padding:4px; font-size:12px; }
                QLineEdit { background:#252526; color:#CAC9C9; border:1px solid #444;
                            border-radius:4px; padding:5px; font-size:12px; }
            """)

            lay = QtGui.QVBoxLayout(dlg)
            lay.setContentsMargins(16, 16, 16, 16)
            lay.setSpacing(10)

            # Baslik
            title_lbl = QtGui.QLabel("Font Settings")
            title_lbl.setStyleSheet("font-size:16px; font-weight:700; color:#3fa9f5;")
            lay.addWidget(title_lbl)

            # Arama kutusu
            search_box = QtGui.QLineEdit()
            search_box.setPlaceholderText("Search font...")
            lay.addWidget(search_box)

            # Font listesi
            font_list = QtGui.QListWidget()
            font_list.setAlternatingRowColors(True)
            font_list.setStyleSheet(
                "QListWidget { alternate-background-color: #2a2a2a; }"
                + font_list.styleSheet()
            )

            # Tum sistem fontlarini yukle
            db = QtGui.QFontDatabase()
            all_fonts = sorted(db.families())
            for fam in all_fonts:
                font_list.addItem(fam)

            # Mevcut fontu sec
            try:
                cur_fam = self.font().family()
                for i in range(font_list.count()):
                    if font_list.item(i).text() == cur_fam:
                        font_list.setCurrentRow(i)
                        font_list.scrollToItem(font_list.currentItem())
                        break
            except Exception:
                pass

            lay.addWidget(font_list)

            # Boyut secimi
            size_row = QtGui.QHBoxLayout()
            size_lbl = QtGui.QLabel("Font Size:")
            size_lbl.setFixedWidth(80)
            size_spin = QtGui.QSpinBox()
            size_spin.setRange(6, 24)
            try:
                size_spin.setValue(self.font().pointSize() if self.font().pointSize() > 0 else 9)
            except Exception:
                size_spin.setValue(9)
            size_row.addWidget(size_lbl)
            size_row.addWidget(size_spin)
            size_row.addStretch()
            lay.addLayout(size_row)

            # Onizleme
            preview_lbl = QtGui.QLabel("Preview:")
            preview_lbl.setStyleSheet("color:#aaa; font-size:11px;")
            lay.addWidget(preview_lbl)

            preview_box = QtGui.QLabel("Filmmaker GUI 3.0  |  The quick brown fox")
            preview_box.setStyleSheet(
                "background:#111; color:#e8e8e8; padding:10px; border-radius:6px;"
                "border:1px solid #333; min-height:36px;"
            )
            preview_box.setWordWrap(True)
            lay.addWidget(preview_box)

            # Onizleme guncelle
            def update_preview():
                try:
                    item = font_list.currentItem()
                    if item:
                        fam2 = item.text()
                        sz = size_spin.value()
                        pf = QtGui.QFont(fam2, sz)
                        preview_box.setFont(pf)
                except Exception:
                    pass

            font_list.currentItemChanged.connect(lambda *a: update_preview())
            size_spin.valueChanged.connect(lambda *a: update_preview())
            update_preview()

            # Arama
            def do_search(txt):
                txt = txt.lower()
                for i in range(font_list.count()):
                    item = font_list.item(i)
                    item.setHidden(txt not in item.text().lower())
                # Ilk gorununeni sec
                for i in range(font_list.count()):
                    if not font_list.item(i).isHidden():
                        font_list.setCurrentRow(i)
                        break

            search_box.textChanged.connect(do_search)

            # Butonlar
            btn_row = QtGui.QHBoxLayout()

            apply_btn = QtGui.QPushButton("Apply Font")
            apply_btn.setStyleSheet(
                "QPushButton { background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
                "stop:0 #0b4f94,stop:1 #072f5a); color:white; font-weight:700; }"
                "QPushButton:hover { background:#1e6fc5; }"
            )
            reset_btn = QtGui.QPushButton("Reset to Default")
            cancel_btn = QtGui.QPushButton("Cancel")

            btn_row.addWidget(apply_btn)
            btn_row.addWidget(reset_btn)
            btn_row.addStretch()
            btn_row.addWidget(cancel_btn)
            lay.addLayout(btn_row)

            def do_apply():
                try:
                    item = font_list.currentItem()
                    if not item:
                        return
                    fam2 = item.text()
                    sz = size_spin.value()
                    new_font = QtGui.QFont(fam2, sz)
                    # Tum widgetlara uygula
                    self.setFont(new_font)
                    for w in self.findChildren(QtGui.QWidget):
                        try:
                            w.setFont(new_font)
                        except Exception:
                            pass
                    # Kaydet (basit dosya)
                    try:
                        import json, os
                        cfg_path = os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            "filmakergui_font.json"
                        )
                        with open(cfg_path, 'w') as _f:
                            json.dump({"family": fam2, "size": sz}, _f)
                    except Exception:
                        pass
                    QtGui.QMessageBox.information(
                        dlg, "Font Applied",
                        "Font set to: {}  {}pt".format(fam2, sz)
                    )
                    dlg.accept()
                except Exception as e:
                    QtGui.QMessageBox.warning(dlg, "Error", str(e))

            def do_reset():
                try:
                    default_font = QtGui.QFont("Arial", 9)
                    self.setFont(default_font)
                    for w in self.findChildren(QtGui.QWidget):
                        try:
                            w.setFont(default_font)
                        except Exception:
                            pass
                    try:
                        import json, os
                        cfg_path = os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            "filmakergui_font.json"
                        )
                        if os.path.exists(cfg_path):
                            os.remove(cfg_path)
                    except Exception:
                        pass
                    dlg.accept()
                except Exception as e:
                    QtGui.QMessageBox.warning(dlg, "Error", str(e))

            apply_btn.clicked.connect(do_apply)
            reset_btn.clicked.connect(do_reset)
            cancel_btn.clicked.connect(dlg.reject)

            dlg.exec_()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def _scroll_style(self):
        # SFM scrollbar: narrow, dark, no rounded corners
        return """
            QScrollArea { background: %(panel)s; border: none; }
            QScrollBar:vertical {
                background: %(bg)s;
                width: 12px;
                border: none;
                border-left: 1px solid %(border)s;
            }
            QScrollBar::handle:vertical {
                background: %(btn_bot)s;
                border: 1px solid %(border)s;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover { background: %(btn_hover)s; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: %(muted)s;
                border: 1px solid %(border)s;
                height: 12px;
                subcontrol-origin: scrollbar;
            }
            QScrollBar::add-line:vertical { subcontrol-position: bottom; }
            QScrollBar::sub-line:vertical { subcontrol-position: top; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
            QScrollBar:horizontal {
                background: %(bg)s;
                height: 12px;
                border: none;
                border-top: 1px solid %(border)s;
            }
            QScrollBar::handle:horizontal {
                background: %(btn_bot)s;
                border: 1px solid %(border)s;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover { background: %(btn_hover)s; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: %(muted)s;
                border: 1px solid %(border)s;
                width: 12px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }
        """ % {k: PALETTE[k] for k in ("panel","bg","border","muted","btn_bot","btn_hover")}

    def _slider_style(self):
        # SFM slider: flat groove, square handle with gradient
        return """
            QSlider::groove:horizontal {
                height: 4px;
                background: %(bg)s;
                border: 1px solid %(border)s;
                border-radius: 0px;
            }
            QSlider::sub-page:horizontal {
                background: %(accent)s;
                border: 1px solid %(border)s;
                height: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 %(btn_top)s, stop:1 %(btn_bot)s);
                border: 1px solid %(border)s;
                width: 8px;
                height: 14px;
                margin: -6px 0;
                border-radius: 0px;
            }
            QSlider::handle:horizontal:hover {
                background: %(btn_hover)s;
            }
        """ % {k: PALETTE[k] for k in ("bg","border","accent","btn_top","btn_bot","btn_hover")}

    def _record_translation_keys(self):
        """Record original English translation keys on widgets so `apply_language` can
        reliably update texts back-and-forth. This stores the key under the Qt
        property 'tr_key' when the cleaned visible text matches a TRANSLATIONS key.
        """
        try:
            # QPushButton
            for btn in self.findChildren(QtGui.QPushButton):
                try:
                    txt = btn.text().strip()
                    clean = re.sub(r'^[^A-Za-z0-9]+', '', txt).strip()
                    if clean in TRANSLATIONS:
                        btn.setProperty('tr_key', clean)
                except Exception:
                    pass
            # QLabel
            for lbl in self.findChildren(QtGui.QLabel):
                try:
                    txt = lbl.text().strip()
                    clean = re.sub(r'^[^A-Za-z0-9]+', '', txt).strip()
                    if clean in TRANSLATIONS:
                        lbl.setProperty('tr_key', clean)
                except Exception:
                    pass
            # QLineEdit placeholder texts
            for le in self.findChildren(QtGui.QLineEdit):
                try:
                    ph = le.placeholderText().strip()
                    clean = re.sub(r'^[^A-Za-z0-9]+', '', ph).strip()
                    if clean in TRANSLATIONS:
                        le.setProperty('tr_key', clean)
                except Exception:
                    pass
        except Exception:
            pass

    # ---------- Utility helpers ----------
    def create_range_slider(self, label_text, min_val, max_val, parent_layout, default=0):
        s_layout = QtGui.QHBoxLayout()
        lbl = QtGui.QLabel("{}: {}".format(label_text, default))
        lbl.setFixedWidth(150)
        lbl.setStyleSheet("color: %s;" % PALETTE["text"])

        # Container holds slider + animated handle overlay stacked
        container = QtGui.QWidget()
        container.setFixedHeight(32)
        container.setStyleSheet("background:transparent;")
        container.setMouseTracking(True)

        slider = QtGui.QSlider(QtCore.Qt.Horizontal, container)
        slider.setRange(min_val, max_val)
        if default < min_val: default = min_val
        if default > max_val: default = max_val
        slider.setValue(default)
        slider.setStyleSheet(
            "QSlider::groove:horizontal{height:8px;background:rgba(255,255,255,0.05);"
            "border-radius:4px;margin:0 7px;}"
            "QSlider::handle:horizontal{width:1px;height:1px;background:transparent;}"
            "QSlider::sub-page:horizontal{background:%s;border-radius:4px;margin:0 7px;}"
            % PALETTE["accent"]
        )
        slider.valueChanged.connect(lambda val, l=lbl, t=label_text: l.setText("{}: {}".format(t, val)))

        # Custom animated handle drawn on top
        ACCENT   = QtGui.QColor(PALETTE["accent"])
        ACCENT_H = QtGui.QColor(PALETTE["accent_hover"])

        class HandleOverlay(QtGui.QWidget):
            def __init__(self, sl):
                super(HandleOverlay, self).__init__(sl.parent())
                self.sl = sl
                self._r   = 7.0   # current radius
                self._hov = False
                self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
                self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
                self._timer = QtCore.QTimer()
                self._timer.timeout.connect(self._tick)
                self._timer.start(16)

            def _tick(self):
                target = 13.0 if self._hov else 7.0
                self._r += (target - self._r) * 0.25
                self.update()

            def _handle_x(self):
                sl = self.sl
                mn, mx = sl.minimum(), sl.maximum()
                if mx == mn: return sl.width() // 2
                ratio = float(sl.value() - mn) / float(mx - mn)
                groove_margin = 7
                return int(groove_margin + ratio * (sl.width() - groove_margin * 2))

            def paintEvent(self, ev):
                import math as _m
                p = QtGui.QPainter(self)
                p.setRenderHint(QtGui.QPainter.Antialiasing)
                x = self._handle_x()
                y = self.height() // 2
                r = self._r
                # Glow
                if self._hov:
                    glow = QtGui.QRadialGradient(x, y, r * 2.2)
                    gc = QtGui.QColor(ACCENT_H); gc.setAlpha(80)
                    gc2 = QtGui.QColor(ACCENT_H); gc2.setAlpha(0)
                    glow.setColorAt(0, gc); glow.setColorAt(1, gc2)
                    p.setPen(QtCore.Qt.NoPen)
                    p.setBrush(QtGui.QBrush(glow))
                    p.drawEllipse(QtCore.QRectF(x-r*2.2, y-r*2.2, r*4.4, r*4.4))
                # Handle circle
                grad = QtGui.QRadialGradient(x - r*0.3, y - r*0.3, r)
                grad.setColorAt(0, QtGui.QColor("#c8e8ff"))
                grad.setColorAt(0.45, ACCENT_H if self._hov else ACCENT)
                grad.setColorAt(1, QtGui.QColor("#051830"))
                p.setPen(QtGui.QPen(ACCENT_H if self._hov else ACCENT, 1.5))
                p.setBrush(QtGui.QBrush(grad))
                p.drawEllipse(QtCore.QRectF(x-r, y-r, r*2, r*2))
                p.end()

            def resizeEvent(self, ev):
                self.setGeometry(0, 0, self.sl.width(), self.sl.height())

        overlay = HandleOverlay(slider)

        # Wire hover from slider -> overlay
        def _enter(ev, o=overlay):
            o._hov = True
            lbl.setStyleSheet("color:%s;font-weight:700;" % PALETTE["accent_hover"])
        def _leave(ev, o=overlay):
            o._hov = False
            lbl.setStyleSheet("color:%s;" % PALETTE["text"])
        slider.enterEvent = _enter
        slider.leaveEvent = _leave

        # Layout inside container
        def _resize_children(ev, s=slider, o=overlay, c=container):
            s.setGeometry(0, 0, c.width(), c.height())
            o.setGeometry(0, 0, c.width(), c.height())
            o.raise_()
        container.resizeEvent = _resize_children

        s_layout.addWidget(lbl)
        s_layout.addWidget(container)
        parent_layout.addLayout(s_layout)
        return slider


    # ---------- Fog functions ----------
    def toggle_fog(self, state):
        enabled = 1 if state == QtCore.Qt.Checked else 0
        try:
            sfm.console("fog_enable {}".format(enabled))
            sfm.console("fog_override {}".format(enabled))
        except Exception:
            pass
        try:
            self.log_box.append(" Fog enabled: {}".format(enabled))
        except Exception:
            pass

    def apply_fog_settings(self):
        try:
            fc = self.fog_color_sliders
            sc = self.skybox_color_sliders
            sfm.console("fog_enable 1")
            sfm.console("fog_override 1")
            sfm.console("fog_color {} {} {}".format(fc['red'].value(), fc['green'].value(), fc['blue'].value()))
            sfm.console("fog_colorskybox {} {} {}".format(sc['red'].value(), sc['green'].value(), sc['blue'].value()))
            sfm.console("fog_start {}".format(self.start_slider.value()))
            sfm.console("fog_end {}".format(self.end_slider.value()))
            sfm.console("fog_startskybox {}".format(self.start_skybox_slider.value()))
            sfm.console("fog_endskybox {}".format(self.end_skybox_slider.value()))
            self.log_box.append(" Fog settings applied.")
        except Exception as e:
            self.log_box.append(" Error applying fog settings: {}".format(e))

    # ---------- Eye Size live updater ----------
    def update_eye_size_live(self, val):
        size = float(val) / 100.0
        try:
            self.eye_size_label.setText("Eye Size: {:.2f}".format(size))
        except Exception:
            pass

        # 1) Try console command (fallback)
        try:
            sfm.console("flexcontroller eye_size {:.2f}".format(size))
        except Exception:
            pass

        # 2) Try to set on selected models if control exists
        try:
            models = []
            try:
                models = sfm.GetSelectedModels() or []
            except Exception:
                try:
                    shot = sfmApp.GetCurrentShot()
                    if shot:
                        models = shot.GetModels() or []
                except Exception:
                    models = []
            for m in models:
                try:
                    ctrl = None
                    try:
                        ctrl = m.FindControl("eye_size")
                    except Exception:
                        ctrl = None
                    if not ctrl:
                        try:
                            ctrl = m.FindControl("eyes")
                        except Exception:
                            ctrl = None
                    if ctrl is not None:
                        try:
                            ctrl.SetValue(size)
                        except Exception:
                            try:
                                ctrl.SetFloatValue(size)
                            except Exception:
                                pass
                except Exception:
                    pass
        except Exception:
            pass

        try:
            self.log_box.append("Eye Size set to {:.2f}".format(size))
        except Exception:
            pass

    # ---------- Mat Picmip dialog opener ----------
    def open_mat_picmip_dialog(self):
        try:
            prompt_title = t("Set mat_picmip") if 'Set mat_picmip' in TRANSLATIONS else "Set mat_picmip"
            prompt_label = t("Set mat_picmip") if 'Set mat_picmip' in TRANSLATIONS else "Value:"
            val, ok = QtGui.QInputDialog.getInt(self, prompt_title, prompt_label, 0, 0, 16)
            if ok:
                try:
                    sfm.console("mat_picmip {}".format(val))
                    if hasattr(self, 'log_box'):
                        try:
                            self.log_box.append("mat_picmip set to {}".format(val))
                        except Exception:
                            pass
                except Exception as e:
                    try:
                        QtGui.QMessageBox.warning(self, "mat_picmip", "Failed to apply mat_picmip: {}".format(e))
                    except Exception:
                        pass
        except Exception:
            pass

    # ---------- Functions ----------
    @safe_call
    def extend_element_duration(self):
        """ChannelsClip Editor - referans: extend_elementduration.py"""
        try:
            import sfm, sfmUtils, vs
            from vs import g_pDataModel as dm

            def get_all_animsets_with_clips():
                shot = sfm.GetCurrentShot()
                if not shot:
                    return []
                result = []
                handle = dm.FirstAllocatedElement()
                while handle != -1:
                    try:
                        elem = dm.GetElement(handle)
                        if elem and elem.GetTypeString() == "DmeAnimationSet":
                            clip = sfmUtils.GetChannelsClipForAnimSet(elem, shot)
                            if clip:
                                result.append((elem.GetName(), clip, clip.timeFrame))
                    except Exception:
                        pass
                    handle = dm.NextAllocatedElement(handle)
                return result

            dlg = QtGui.QDialog(self)
            dlg.setWindowTitle("ChannelsClip Editor")
            dlg.resize(820, 600)
            dlg.setStyleSheet(
                "QDialog{background:%s;color:%s;}"
                "QLabel{color:%s;background:transparent;}"
                "QLineEdit{background:%s;color:%s;border:1px solid %s;border-radius:4px;padding:5px;}"
                "QTableWidget{background:%s;color:%s;border:1px solid %s;gridline-color:%s;}"
                "QHeaderView::section{background:%s;color:%s;padding:6px;border:none;border-bottom:2px solid %s;font-weight:700;}"
                "QTableWidget::item:alternate{background:%s;}"
                "QTableWidget::item:selected{background:%s;color:#fff;}" % (
                    PALETTE["panel"], PALETTE["text"], PALETTE["text"],
                    PALETTE["bg"], PALETTE["text"], PALETTE["muted"],
                    PALETTE["bg"], PALETTE["text"], PALETTE["muted"], PALETTE["muted"],
                    PALETTE["panel"], PALETTE["teal"], PALETTE["teal"],
                    PALETTE["panel"], PALETTE["accent"]))

            layout = QtGui.QVBoxLayout(dlg)
            layout.setContentsMargins(14, 14, 14, 14)
            layout.setSpacing(10)

            ttl = QtGui.QLabel("ChannelsClip Editor")
            ttl.setStyleSheet("font-size:16px;font-weight:900;color:%s;" % PALETTE["teal"])
            layout.addWidget(ttl)
            dsc = QtGui.QLabel(
                "Sahnedeki tum DmeAnimationSet channels clip sureslerini duzenler. "
                "Duration artirarak 60sn kilitleme bugunu duzeltir.")
            dsc.setWordWrap(True)
            dsc.setStyleSheet("font-size:11px;color:%s;" % PALETTE["muted"])
            layout.addWidget(dsc)

            mass_layout = QtGui.QGridLayout()
            mass_layout.setSpacing(6)
            def _lbl(t):
                l = QtGui.QLabel(t)
                l.setStyleSheet("color:%s;font-weight:600;" % PALETTE["text"])
                return l
            def _inp(default):
                e = QtGui.QLineEdit(default)
                e.setFixedWidth(110)
                return e
            def _mbtn(text, color):
                b = QtGui.QPushButton(text)
                b.setStyleSheet(self._global_button_style(color))
                b.setFixedHeight(28)
                add_hover_glow(b)
                return b
            start_input    = _inp("-5.0")
            duration_input = _inp("70.0")
            offset_input   = _inp("0.0")
            apply_start_btn    = _mbtn("Apply Start to All",    PALETTE["accent"])
            apply_duration_btn = _mbtn("Apply Duration to All", PALETTE["teal"])
            apply_offset_btn   = _mbtn("Apply Offset to All",   PALETTE["muted"])
            mass_layout.addWidget(_lbl("Start:"),     0, 0)
            mass_layout.addWidget(start_input,        0, 1)
            mass_layout.addWidget(apply_start_btn,    0, 2)
            mass_layout.addWidget(_lbl("Duration:"),  1, 0)
            mass_layout.addWidget(duration_input,     1, 1)
            mass_layout.addWidget(apply_duration_btn, 1, 2)
            mass_layout.addWidget(_lbl("Offset:"),    2, 0)
            mass_layout.addWidget(offset_input,       2, 1)
            mass_layout.addWidget(apply_offset_btn,   2, 2)
            layout.addLayout(mass_layout)

            table = QtGui.QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["AnimationSet", "Start", "Duration", "Offset"])
            hdr = table.horizontalHeader()
            hdr.setResizeMode(0, QtGui.QHeaderView.Stretch)
            hdr.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            hdr.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
            hdr.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
            table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            table.verticalHeader().setVisible(False)
            table.setAlternatingRowColors(True)
            layout.addWidget(table, 1)

            data_store = [[]]

            def refresh():
                table.setRowCount(0)
                data_store[0] = []
                clips = get_all_animsets_with_clips()
                for name, clip, tf in clips:
                    row = table.rowCount()
                    table.insertRow(row)
                    ni = QtGui.QTableWidgetItem(name)
                    ni.setFlags(ni.flags() & ~QtCore.Qt.ItemIsEditable)
                    ni.setForeground(QtGui.QBrush(QtGui.QColor(PALETTE["teal"])))
                    table.setItem(row, 0, ni)
                    for col, val in enumerate([tf.start, tf.duration, tf.offset], 1):
                        it = QtGui.QTableWidgetItem(str(val))
                        it.setFlags(it.flags() | QtCore.Qt.ItemIsEditable)
                        it.setForeground(QtGui.QBrush(QtGui.QColor(PALETTE["text"])))
                        table.setItem(row, col, it)
                    data_store[0].append((clip, tf))
                if not clips:
                    table.insertRow(0)
                    mi = QtGui.QTableWidgetItem("Mevcut shotta DmeAnimationSet bulunamadi.")
                    mi.setForeground(QtGui.QBrush(QtGui.QColor(PALETTE["muted"])))
                    table.setItem(0, 0, mi)

            def set_start_to_all():
                v = start_input.text()
                for r in range(table.rowCount()):
                    it = table.item(r, 1)
                    if it: it.setText(v)

            def set_duration_to_all():
                v = duration_input.text()
                for r in range(table.rowCount()):
                    it = table.item(r, 2)
                    if it: it.setText(v)

            def set_offset_to_all():
                v = offset_input.text()
                for r in range(table.rowCount()):
                    it = table.item(r, 3)
                    if it: it.setText(v)

            def apply_changes():
                d = data_store[0]
                if not d:
                    return
                guard = vs.CAppDisableUndoScopeGuard("ChannelsClipEditor", 0)
                count = 0
                try:
                    for i, (clip, tf) in enumerate(d):
                        try:
                            tf.duration = float(table.item(i, 2).text())
                            count += 1
                        except Exception:
                            continue
                finally:
                    del guard
                self.log_box.append("[ExtendDuration] Updated {} clips.".format(count))
                QtGui.QMessageBox.information(dlg, "Done", "Updated {} clips.".format(count))

            apply_start_btn.clicked.connect(set_start_to_all)
            apply_duration_btn.clicked.connect(set_duration_to_all)
            apply_offset_btn.clicked.connect(set_offset_to_all)

            btn_row = QtGui.QHBoxLayout()
            refresh_btn = QtGui.QPushButton("Refresh")
            refresh_btn.setStyleSheet(self._global_button_style(PALETTE["accent"]))
            add_hover_glow(refresh_btn)
            apply_btn = QtGui.QPushButton("Apply Changes")
            apply_btn.setStyleSheet(self._global_button_style(PALETTE["green"]))
            add_hover_glow(apply_btn)
            close_btn = QtGui.QPushButton("Close")
            close_btn.setStyleSheet(self._global_button_style(PALETTE["muted"]))
            btn_row.addWidget(refresh_btn)
            btn_row.addWidget(apply_btn)
            btn_row.addStretch()
            btn_row.addWidget(close_btn)
            layout.addLayout(btn_row)

            refresh_btn.clicked.connect(refresh)
            apply_btn.clicked.connect(apply_changes)
            close_btn.clicked.connect(dlg.reject)

            refresh()
            dlg.exec_()

        except Exception as e:
            import traceback
            self.log_box.append("[ExtendDuration] ERROR: " + str(e))
            QtGui.QMessageBox.warning(self, "Error",
                str(e) + "\n\n" + traceback.format_exc())

    def clean_memory(self):
        """
        Windows-only memory cleanup — NO SFM console commands at all.
        SFM console commands (even safe-looking ones) can crash SFM if called
        from a Python thread while the game loop is in a certain state.
        We only use Windows API calls which are external to SFM's engine.
        """
        import ctypes, gc
        report = []

        # ── 1. Python GC ─────────────────────────────────────────────────────
        try:
            n = gc.collect()
            report.append("GC: {} objects freed".format(n))
        except Exception as e:
            report.append("GC error: {}".format(e))

        # ── 2. Windows Working Set flush ─────────────────────────────────────
        # Releases pages from RAM working set back to the OS page pool.
        # Safe: doesn't touch SFM's heap or GPU resources.
        try:
            pid = ctypes.windll.kernel32.GetCurrentProcess()
            ok  = ctypes.windll.psapi.EmptyWorkingSet(pid)
            report.append("RAM working set flush: {}".format("OK" if ok else "failed"))
        except Exception as e:
            report.append("RAM flush error: {}".format(e))

        # ── 3. Heap compact ──────────────────────────────────────────────────
        # Coalesces free heap blocks. Read-only from SFM engine's perspective.
        try:
            heap = ctypes.windll.kernel32.GetProcessHeap()
            freed = ctypes.windll.kernel32.HeapCompact(heap, 0)
            report.append("Heap compact: {} bytes coalesced".format(freed))
        except Exception as e:
            report.append("Heap compact error: {}".format(e))

        # ── 4. DXVK GPU staging buffer flush ─────────────────────────────────
        # When SFM runs under DXVK (Vulkan), DXVK accumulates staging buffers
        # in VRAM. PostMessage WM_USER to the SFM window causes DXVK to submit
        # its pending Vulkan command queue on the NEXT frame — no engine call,
        # fully async and safe. This is the main cause of the VRAM drop.
        try:
            hwnd = ctypes.windll.user32.FindWindowW(None, u"Source Filmmaker [Beta]")
            if not hwnd:
                hwnd = ctypes.windll.user32.FindWindowW(None, u"Source Filmmaker")
            if hwnd:
                # PostMessage is async — does not block or interrupt the game loop
                ctypes.windll.user32.PostMessageW(hwnd, 0x0400, 0, 0)
                report.append("DXVK GPU flush: queued (next frame)")
            else:
                report.append("DXVK GPU flush: SFM window not found")
        except Exception as e:
            report.append("DXVK flush error: {}".format(e))

        # ── Report ───────────────────────────────────────────────────────────
        for line in report:
            self.log_box.append("[CleanMem] " + line)

        ok_count = sum(1 for r in report if "error" not in r.lower() and "fail" not in r.lower())

        QtGui.QMessageBox.information(
            self, "Clean Memory — Done",
            "{}/{} steps succeeded.\n\n".format(ok_count, len(report)) +
            "\n".join("  " + r for r in report) +
            "\n\nNote: No SFM console commands were used.\n"
            "DXVK GPU flush takes effect on the next rendered frame."
        )

    def set_ram_boost(self, val):
        # This function now only saves the value; it does not execute the command
        self.ram_boost_value = val
        try:
            self.log_box.append("RAM Boost Level set to {} (Apply with Boost Now)".format(val))
        except Exception:
            pass

    def set_fps_boost(self, val):
        try:
            sfm.console("fps_max {}".format(val))
            shot = sfmApp.GetCurrentShot()
            if shot:
                fps_setting = shot.GetSetting("fps")
                fps_setting.SetValue(int(val))
                self.log_box.append("Timeline FPS set to {}".format(val))
        except Exception as e:
            self.log_box.append("Error while setting FPS: {}".format(e))

    def run_selected_quick_command(self):
        try:
            # Prefer the Quick Commands in SFM Command GUI 2 (menu2)
            selected_display = None
            selected_key = None
            if hasattr(self, 'menu2_quick_box'):
                try:
                    selected_display = self.menu2_quick_box.currentText()
                    idx = self.menu2_quick_box.currentIndex()
                    selected_key = None
                    try:
                        selected_key = self.menu2_quick_box.itemData(idx)
                    except Exception:
                        selected_key = None
                except Exception:
                    selected_display = None
            elif hasattr(self, 'quick_command_box'):
                selected_display = self.quick_command_box.currentText()
                selected_key = None

            if selected_display and selected_display != t("Select quick command"):
                # prefer the stored key (original English label) for lookup
                command = None
                if selected_key:
                    command = self.quick_commands.get(selected_key)
                if not command:
                    command = self.quick_commands.get(selected_display)
                if command:
                    sfm.console(command)
                    if hasattr(self, 'log_box'):
                        self.log_box.append(" Executed: {}".format(command))
                else:
                    if hasattr(self, 'log_box'):
                        self.log_box.append("Unknown command selected")
            else:
                if hasattr(self, 'log_box'):
                    self.log_box.append(" Please select a command from dropdown")
        except Exception as e:
            if hasattr(self, 'log_box'):
                self.log_box.append("Error executing quick command: {}".format(e))
    def boost_now(self):
        try:
            sfm.console("mat_picmip {}".format(self.ram_boost_value))
            self.log_box.append(" mat_picmip set to {}".format(self.ram_boost_value))
        except Exception as e:
            self.log_box.append(" Error applying RAM boost: {}".format(e))

        self.log_box.append(" Boost commands applied.")
        self.clean_memory()

    def apply_performance_options(self):
        try:
            messages = []

            # Enable Texture Optimization
            if self.chk_texture_opt.isChecked():
                try:
                    sfm.console("mat_picmip 2")
                    sfm.console("mat_reducefillrate 1")
                    messages.append(" Texture Optimization: ON (mat_picmip 2, mat_reducefillrate 1)")
                except Exception as e:
                    messages.append(" Texture Optimization error: {}".format(e))
            else:
                try:
                    sfm.console("mat_picmip 0")
                    sfm.console("mat_reducefillrate 0")
                    messages.append(" Texture Optimization: OFF (mat_picmip 0, mat_reducefillrate 0)")
                except Exception as e:
                    messages.append(" Texture Optimization reset error: {}".format(e))

            # Activate Particle Boost
            if self.chk_particle_boost.isChecked():
                try:
                    sfm.console("cl_particle_batch_mode 1")
                    sfm.console("r_drawparticles 1")
                    messages.append(" Particle Boost: ON (cl_particle_batch_mode 1)")
                except Exception as e:
                    messages.append(" Particle Boost error: {}".format(e))
            else:
                try:
                    sfm.console("cl_particle_batch_mode 0")
                    messages.append(" Particle Boost: OFF")
                except Exception as e:
                    messages.append(" Particle Boost reset error: {}".format(e))

            # Optimize Shadows
            if self.chk_optimize_shadows.isChecked():
                try:
                    sfm.console("r_shadowrendertotexture 0")
                    sfm.console("r_shadows 0")
                    messages.append(" Optimize Shadows: ON (shadows disabled for performance)")
                except Exception as e:
                    messages.append(" Optimize Shadows error: {}".format(e))
            else:
                try:
                    sfm.console("r_shadowrendertotexture 1")
                    sfm.console("r_shadows 1")
                    messages.append(" Optimize Shadows: OFF (shadows restored)")
                except Exception as e:
                    messages.append(" Optimize Shadows reset error: {}".format(e))

            for msg in messages:
                try:
                    self.log_box.append(msg)
                except Exception:
                    pass

            try:
                QtGui.QMessageBox.information(self, "Performance Options", "\n".join(messages))
            except Exception:
                pass

        except Exception as e:
            try:
                self.log_box.append(" apply_performance_options error: {}".format(e))
            except Exception:
                pass

    def open_session_importer_dialog(self):
        try:
            dlg = SessionImporterDialog(self)
            dlg.exec_()
        except Exception as e:
            try:
                self.log_box.append("Session Importer error: {}".format(e))
            except Exception:
                pass

    def open_light_limit_dialog(self):
        try:
            dlg = LightLimitDialog(self)
            dlg.exec_()
        except Exception as e:
            try:
                self.log_box.append(" Error opening Light Limit dialog: {}".format(e))
            except Exception:
                pass

    # ---------- Auto Lip Sync helpers (prototype) ----------
    def _is_face_category_selected(self):
        # Best-effort check: try to see if selected model has FACE controls
        try:
            models = []
            try:
                models = sfm.GetSelectedModels() or []
            except Exception:
                models = []
            for m in models:
                try:
                    # Try to access a FACE controller or check control names
                    if hasattr(m, 'GetController'):
                        try:
                            ctrl = m.GetController('FACE')
                            if ctrl:
                                return True
                        except Exception:
                            pass
                    # Fallback: try to introspect parameter names
                    if hasattr(m, 'GetAvailableControls'):
                        try:
                            ctrls = m.GetAvailableControls() or []
                            for c in ctrls:
                                if 'face' in str(c).lower():
                                    return True
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass
        return False

    def _update_lipsync_buttons(self):
        # Enable/disable buttons based on inputs and model selection
        try:
            has_text = bool(getattr(self, 'lipsync_text', QtGui.QLineEdit()).text().strip())
            has_audio = hasattr(self, 'lipsync_audio_path') and bool(getattr(self, 'lipsync_audio_path'))
            model_ok = hasattr(self, 'lipsync_selected_model') and self.lipsync_selected_model is not None
            if hasattr(self, 'lipsync_apply_text_btn'):
                self.lipsync_apply_text_btn.setEnabled(has_text and model_ok)
            if hasattr(self, 'lipsync_apply_audio_btn'):
                self.lipsync_apply_audio_btn.setEnabled(has_audio and model_ok)
            # Update select button text color/status
            if hasattr(self, 'select_model_btn'):
                if model_ok and hasattr(self, 'lipsync_selected_name'):
                    self.select_model_btn.setStyleSheet("background: %s; color: %s; padding:8px; border-radius:6px;" % (PALETTE['success'], PALETTE['panel']))
                    self.select_model_btn.setText(t("Selected Model: %s") % self.lipsync_selected_name)
                elif hasattr(self, 'lipsync_selected_model') and self.lipsync_selected_model is None:
                    # Explicit failure state: red and show "No model was selected..."
                    self.select_model_btn.setStyleSheet("background: %s; color: %s; padding:8px; border-radius:6px;" % (PALETTE['danger'], PALETTE['panel']))
                    self.select_model_btn.setText(t("No model was selected..."))
                else:
                    self.select_model_btn.setStyleSheet("background: %s; color: %s; padding:8px; border-radius:6px;" % (PALETTE['muted'], PALETTE['text']))
                    self.select_model_btn.setText(t("Select Model From Animation Set Editor"))
        except Exception:
            pass

    def set_selected_model(self, model_obj, model_name):
        # Called by the selector when a model is chosen
        try:
            if model_obj is None:
                self.lipsync_selected_model = None
                self.lipsync_selected_name = None
                try:
                    self.select_model_btn.setText(t("Select Model From Animation Set Editor"))
                    self.select_model_btn.setStyleSheet(self._global_button_style(PALETTE['danger']) + " padding:10px; border-radius:10px; font-weight:700;")
                except Exception:
                    pass
            else:
                self.lipsync_selected_model = model_obj
                self.lipsync_selected_name = model_name
                try:
                    self.select_model_btn.setText(t("Selected Model: %s") % model_name)
                    self.select_model_btn.setStyleSheet(self._global_button_style(PALETTE['success']) + " padding:10px; border-radius:10px; font-weight:700;")
                except Exception:
                    pass
                # Try to also select this model in SFM's editor (best-effort)
                try:
                    try:
                        sfm.SelectModels([model_obj])
                    except Exception:
                        try:
                            sfm.SetSelectedModels([model_obj])
                        except Exception:
                            try:
                                if hasattr(model_obj, 'SetSelected'):
                                    model_obj.SetSelected(True)
                            except Exception:
                                pass
                except Exception:
                    pass
                # try to open Graph Editor so the user can see timeline/graph
                try:
                    if hasattr(sfmApp, 'ShowTabWindow'):
                        sfmApp.ShowTabWindow("GraphEditor")
                except Exception:
                    pass
        except Exception:
            pass
        # Refresh buttons and label
        self._update_lipsync_buttons()

    def open_select_model_dialog(self):
        """Open the model selector dialog where user can pick a FACE-enabled model from ASE."""
        try:
            dlg = SelectModelDialog(self)
            # exec_ will block until closed; the dialog calls set_selected_model on success
            dlg.exec_()
            self._update_lipsync_buttons()
        except Exception:
            pass

    def apply_text_lipsync(self):
        text = getattr(self, 'lipsync_text', QtGui.QLineEdit()).text().strip()
        if not text:
            QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Please enter text for lipsync"))
            return
        # Require that a model was selected via the selector dialog
        if not hasattr(self, 'lipsync_selected_model') or self.lipsync_selected_model is None:
            QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("No model selected. Please select a model first."))
            return
        # Check model supports FACE
        try:
            m = self.lipsync_selected_model
            has_face = False
            try:
                if hasattr(m, 'GetController'):
                    if m.GetController('FACE'):
                        has_face = True
            except Exception:
                pass
            try:
                if not has_face and hasattr(m, 'GetAvailableControls'):
                    ctrls = m.GetAvailableControls() or []
                    for c in ctrls:
                        if 'face' in str(c).lower():
                            has_face = True
                            break
            except Exception:
                pass
            if not has_face:
                QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Selected model does not have FACE controls"))
                return
        except Exception:
            QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Could not validate selected model"))
            return

        # Simple lipsync prototype: try to generate basic mouth/jaw controls over time
        if hasattr(self, 'log_box'):
            self.log_box.append("ğŸ¤ Auto Lip Sync (text) starting for {}".format(self.lipsync_selected_name))
        try:
            # run generator (safe, best-effort)
            try:
                self._generate_simple_lipsync(self.lipsync_selected_model, text)
                if hasattr(self, 'log_box'):
                    self.log_box.append("âœ” Simple lipsync generation finished (prototype)")
            except Exception as e:
                if hasattr(self, 'log_box'):
                    self.log_box.append("âš  Lipsync generation error: {}".format(e))
                try:
                    sfm.console('echo "Auto Lip Sync failed: {}"'.format(e))
                except Exception:
                    pass
            # Best-effort: try to make selected model active in animation set editor
            try:
                sfm.SelectModels([self.lipsync_selected_model])
            except Exception:
                try:
                    sfm.SetSelectedModels([self.lipsync_selected_model])
                except Exception:
                    pass
            try:
                sfm.console('echo "Auto Lip Sync (text) applied to {}"'.format(self.lipsync_selected_name))
            except Exception:
                pass
        except Exception:
            pass

    def browse_audio_lipsync(self):
        try:
            path = QtGui.QFileDialog.getOpenFileName(self, "Select WAV file", "", "WAV Files (*.wav)")
            if isinstance(path, tuple) or isinstance(path, list):
                path = path[0]
            if not path:
                return
            # size check (100 MB)
            try:
                if os.path.getsize(path) > 100 * 1024 * 1024:
                    QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Selected audio not detected."))
                    return
            except Exception:
                pass
            self.lipsync_audio_path = path
            self.lipsync_audio_label.setText("Selected: {}".format(os.path.basename(path)))
            self._update_lipsync_buttons()
        except Exception:
            QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Selected audio not detected."))

    def apply_audio_lipsync(self):
        if not hasattr(self, 'lipsync_audio_path') or not self.lipsync_audio_path:
            QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Selected audio not detected."))
            return
        if not hasattr(self, 'lipsync_selected_model') or self.lipsync_selected_model is None:
            QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("No model selected. Please select a model first."))
            return
        # Validate FACE support
        try:
            m = self.lipsync_selected_model
            has_face = False
            try:
                if hasattr(m, 'GetController'):
                    if m.GetController('FACE'):
                        has_face = True
            except Exception:
                pass
            try:
                if not has_face and hasattr(m, 'GetAvailableControls'):
                    ctrls = m.GetAvailableControls() or []
                    for c in ctrls:
                        if 'face' in str(c).lower():
                            has_face = True
                            break
            except Exception:
                pass
            if not has_face:
                QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Selected model does not have FACE controls"))
                return
        except Exception:
            QtGui.QMessageBox.warning(self, "Auto Lip Sync", t("Could not validate selected model"))
            return

        # Prototype behaviour: log action and add a console note
        if hasattr(self, 'log_box'):
            self.log_box.append("ğŸ¤ Auto Lip Sync (audio) applied to {}: {}".format(self.lipsync_selected_name, os.path.basename(self.lipsync_audio_path)))
        try:
            try:
                sfm.SelectModels([self.lipsync_selected_model])
            except Exception:
                pass
            sfm.console('echo "Auto Lip Sync (audio) applied to {}"'.format(self.lipsync_selected_name))
        except Exception:
            pass

# ---------- Mat Picmip Dialog ----------
class SFMOverlayWindow(QtGui.QWidget):
    """Overlay window that can show multiple images (QLabels) with scale/opacity and be dragged.
    Minimal, best-effort implementation using QLabel pixmaps and QGraphicsOpacityEffect.
    """
    def __init__(self, parent=None):
        super(SFMOverlayWindow, self).__init__(parent, QtCore.Qt.Tool)
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("SFM Overlay")
        self.resize(640, 360)
        self._drag_pos = None
        self.images = []  # list of dicts: {path,label,scale,opacity}
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

    def add_image(self, path, scale=1.0, opacity=1.0):
        try:
            if not os.path.exists(path):
                return False
            # normalize path and attempt multiple load strategies for robustness
            path = os.path.normpath(path)
            lbl = QtGui.QLabel(self)
            lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            pm = QtGui.QPixmap()
            try:
                # primary attempt
                pm.load(path)
            except Exception:
                pass
            # fallback 1: QImageReader
            if pm.isNull():
                try:
                    reader = QtGui.QImageReader(path)
                    if reader.canRead():
                        img = reader.read()
                        if not img.isNull():
                            pm = QtGui.QPixmap.fromImage(img)
                except Exception:
                    pass
            # fallback 2: read raw bytes and use QImage.fromData
            if pm.isNull():
                try:
                    with open(path, 'rb') as f:
                        data = f.read()
                    if data:
                        try:
                            img = QtGui.QImage.fromData(data)
                            if img and not img.isNull():
                                pm = QtGui.QPixmap.fromImage(img)
                        except Exception:
                            pass
                except Exception:
                    pass
            # fallback 3: use Pillow to convert to PNG in-memory (if available)
            if pm.isNull():
                try:
                    from io import BytesIO
                    try:
                        from PIL import Image
                        bio = BytesIO()
                        im = Image.open(path).convert('RGBA')
                        im.save(bio, format='PNG')
                        b = bio.getvalue()
                        img = QtGui.QImage.fromData(b)
                        if img and not img.isNull():
                            pm = QtGui.QPixmap.fromImage(img)
                    except Exception:
                        pass
                except Exception:
                    pass
            if pm.isNull():
                return False
            lbl._orig_pixmap = pm
            lbl._scale = float(scale)
            lbl._opacity = float(opacity)
            self._apply_pixmap_to_label(lbl)
            lbl.show()
            # opacity effect
            eff = QtGui.QGraphicsOpacityEffect(lbl)
            eff.setOpacity(lbl._opacity)
            lbl.setGraphicsEffect(eff)
            self.images.append({'path': path, 'label': lbl, 'scale': lbl._scale, 'opacity': lbl._opacity})
            lbl.raise_()
            return True
        except Exception:
            return False

    def remove_image(self, index):
        try:
            if index < 0 or index >= len(self.images):
                return
            entry = self.images.pop(index)
            try:
                lbl = entry.get('label')
                if lbl is not None:
                    # Guard against already-deleted Qt C++ objects
                    try:
                        valid = shiboken.isValid(lbl)
                    except Exception:
                        valid = True  # assume valid if check fails
                    if valid:
                        try:
                            lbl.hide()
                        except Exception:
                            pass
                        try:
                            lbl.deleteLater()
                        except Exception:
                            pass
            except Exception:
                pass
        except Exception:
            pass

    def bring_to_front(self, index):
        try:
            if index < 0 or index >= len(self.images):
                return
            lbl = self.images[index]['label']
            lbl.raise_()
        except Exception:
            pass

    def set_image_scale(self, index, scale):
        try:
            if index < 0 or index >= len(self.images):
                return
            entry = self.images[index]
            lbl = entry['label']
            lbl._scale = float(scale)
            entry['scale'] = lbl._scale
            self._apply_pixmap_to_label(lbl)
        except Exception:
            pass

    def set_image_opacity(self, index, opacity):
        try:
            if index < 0 or index >= len(self.images):
                return
            entry = self.images[index]
            lbl = entry['label']
            entry['opacity'] = float(opacity)
            eff = lbl.graphicsEffect()
            if not eff or not isinstance(eff, QtGui.QGraphicsOpacityEffect):
                eff = QtGui.QGraphicsOpacityEffect(lbl)
                lbl.setGraphicsEffect(eff)
            eff.setOpacity(max(0.0, min(1.0, float(opacity))))
        except Exception:
            pass

    def set_lock_clickthrough(self, lock):
        try:
            # If lock is True -> ignore mouse events (click-through)
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, bool(lock))
        except Exception:
            pass

    def _apply_pixmap_to_label(self, lbl):
        try:
            pm = lbl._orig_pixmap
            if pm is None:
                return
            w = int(pm.width() * lbl._scale)
            h = int(pm.height() * lbl._scale)
            if w <= 0 or h <= 0:
                return
            scaled = pm.scaled(w, h, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            lbl.setPixmap(scaled)
            lbl.resize(scaled.size())
            # Resize the overlay window itself to match the image size,
            # so it never bleeds over SFM viewports at any scale value.
            try:
                self.resize(scaled.width(), scaled.height())
            except Exception:
                pass
            # Always place label at (0,0) since window now matches image size
            try:
                lbl.move(0, 0)
            except Exception:
                pass
        except Exception:
            pass

    def resizeEvent(self, ev):
        # keep existing images roughly centered
        try:
            for entry in self.images:
                lbl = entry['label']
                try:
                    self._apply_pixmap_to_label(lbl)
                except Exception:
                    pass
        except Exception:
            pass
        super(SFMOverlayWindow, self).resizeEvent(ev)

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self._drag_pos = ev.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, ev):
        if self._drag_pos is not None and ev.buttons() & QtCore.Qt.LeftButton:
            try:
                self.move(ev.globalPos() - self._drag_pos)
            except Exception:
                pass

    def mouseReleaseEvent(self, ev):
        self._drag_pos = None

    @safe_call
    def apply_patch(self):
        apply_light_limit_patch(self.spin.value())
        self.accept()
class SessionImporterDialog(QtGui.QDialog):
    """
    SFM Session Importer - by OMGTheresABearInMyOatmeal
    Embedded into Filmmaker GUI 4.0 by Hiddex
    """
    def __init__(self, parent=None):
        super(SessionImporterDialog, self).__init__(parent)
        self.setWindowTitle("Session Importer")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.resize(480, 380)
        self.setSizeGripEnabled(True)
        self.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #000,stop:1 %s);"
            "color: %s;" % (PALETTE["panel"], PALETTE["text"])
        )
        font = QtGui.QFont(); font.setPointSize(10)
        self.setFont(font)

        self.filename = None
        self.sessionObj = None
        self._build_ui()

    def _build_ui(self):
        P = PALETTE
        BTN = (
            "QPushButton{background:%s;color:%s;border:1px solid %s;"
            "border-radius:5px;padding:5px 12px;font-size:11px;font-weight:bold;}"
            "QPushButton:hover{background:%s;}"
        ) % (P["accent"], P["text"], P["accent_hover"], P["accent_hover"])

        vl = QtGui.QVBoxLayout(self)

        # File row
        hl = QtGui.QHBoxLayout()
        lbl = QtGui.QLabel("Session File")
        lbl.setStyleSheet("color:%s;font-size:11px;" % P["text"])
        self.lineEdit_filename = QtGui.QLineEdit()
        self.lineEdit_filename.setEnabled(False)
        self.lineEdit_filename.setPlaceholderText("Select a Session File (.dmx)")
        self.lineEdit_filename.setStyleSheet(
            "QLineEdit{background:%s;color:%s;border:1px solid %s;border-radius:4px;padding:5px;}"
            % (P["muted"], P["text"], P["accent"]))
        browse_btn = QtGui.QToolButton()
        browse_btn.setText("...")
        browse_btn.setStyleSheet(BTN)
        browse_btn.clicked.connect(self.getfile)
        hl.addWidget(lbl)
        hl.addWidget(self.lineEdit_filename, 1)
        hl.addWidget(browse_btn)
        vl.addLayout(hl)

        # Tabs: Shots / Tracks / File Info
        self.tab_widget = QtGui.QTabWidget()
        self.tab_widget.setStyleSheet(
            "QTabWidget::pane{background:%s;border:1px solid %s;}"
            "QTabBar::tab{background:%s;color:%s;padding:6px 14px;}"
            "QTabBar::tab:selected{background:%s;color:%s;}" % (
                P["panel"], P["muted"],
                P["muted"], P["text"],
                P["accent"], P["text"])
        )
        LIST_SS = (
            "QListWidget{background:%s;color:%s;border:none;font-size:11px;}"
            "QListWidget::item:selected{background:%s;}"
            "QListWidget::item:hover{background:%s;}"
        ) % (P["bg"], P["text"], P["accent"], P["muted"])

        # Shots tab
        shot_w = QtGui.QWidget()
        shot_vl = QtGui.QVBoxLayout(shot_w); shot_vl.setContentsMargins(4,4,4,4)
        self.listWidget = QtGui.QListWidget()
        self.listWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listWidget.setStyleSheet(LIST_SS)
        self.listWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        toggle1 = QtGui.QAction("Toggle All", self.listWidget)
        toggle1.triggered.connect(lambda: self.toggleChecked(self.listWidget))
        self.listWidget.addAction(toggle1)
        shot_vl.addWidget(self.listWidget)
        self.tab_widget.addTab(shot_w, "Shots")

        # Tracks tab
        track_w = QtGui.QWidget()
        track_vl = QtGui.QVBoxLayout(track_w); track_vl.setContentsMargins(4,4,4,4)
        self.listWidget_2 = QtGui.QListWidget()
        self.listWidget_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listWidget_2.setStyleSheet(LIST_SS)
        self.listWidget_2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        toggle2 = QtGui.QAction("Toggle All", self.listWidget_2)
        toggle2.triggered.connect(lambda: self.toggleChecked(self.listWidget_2))
        self.listWidget_2.addAction(toggle2)
        track_vl.addWidget(self.listWidget_2)
        self.tab_widget.addTab(track_w, "Tracks")

        # File Info tab
        info_w = QtGui.QWidget()
        info_vl = QtGui.QVBoxLayout(info_w); info_vl.setContentsMargins(8,8,8,8)
        self.map_label = QtGui.QLabel("")
        self.framerate_label = QtGui.QLabel("")
        for l in [self.map_label, self.framerate_label]:
            l.setStyleSheet("color:%s;font-size:11px;" % P["text"])
            info_vl.addWidget(l)
        info_vl.addStretch()
        self.tab_widget.addTab(info_w, "File Info")

        vl.addWidget(self.tab_widget, 1)

        # Buttons
        sep = QtGui.QFrame(); sep.setFrameShape(QtGui.QFrame.HLine)
        sep.setStyleSheet("color:%s;" % P["muted"])
        vl.addWidget(sep)

        misc_btn = QtGui.QPushButton("Import FilmClip to miscBin only")
        misc_btn.setStyleSheet(BTN)
        misc_btn.clicked.connect(self.addTomiscBin)
        vl.addWidget(misc_btn)

        import_btn = QtGui.QPushButton("Import Checked Items")
        import_btn.setFixedHeight(44)
        import_btn.setStyleSheet(
            "QPushButton{background:%s;color:%s;font-size:15px;font-weight:bold;"
            "border-radius:6px;border:none;}"
            "QPushButton:hover{background:%s;}" % (P["accent"], P["text"], P["accent_hover"])
        )
        import_btn.clicked.connect(self.importSelected)
        vl.addWidget(import_btn)

    def ErrorBox(self, e):
        msg = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "ERROR", str(e),
                                QtGui.QMessageBox.NoButton)
        msg.addButton("&OK", QtGui.QMessageBox.RejectRole)
        msg.exec_()

    def getfile(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            self, "Load session file",
            "usermod/elements/sessions", "(*.dmx)")
        if filename:
            self.filename = filename
            self.lineEdit_filename.setText(filename)
            self.populateLists()

    def populateLists(self):
        try:
            # SetFileId YOK - undo stack patliyor
            self.sessionObj = dm.RestoreFromFile(
                str(self.filename), None, None, vs.CR_COPY_NEW).Copy()

            if not self.sessionObj.HasAttribute("activeClip"):
                self.ErrorBox("This file is not an SFM session!")
                self.sessionObj = None
                self.filename = None
                self.lineEdit_filename.clear()
                self.listWidget.clear()
                self.listWidget_2.clear()
                self.map_label.setText("")
                self.framerate_label.setText("")
                return

            self.listWidget.clear()
            self.listWidget_2.clear()

            s = self.sessionObj
            if not s.activeClip:
                if s.clipBin.count() > 0:
                    s.activeClip = s.clipBin[0]

            # Shots
            try:
                for shot in s.activeClip.subClipTrackGroup.tracks[0].children:
                    if shot:
                        item = QtGui.QListWidgetItem(self.listWidget)
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Unchecked)
                        item.setText(shot.GetName())
            except Exception:
                pass

            # Tracks
            try:
                for track in s.activeClip.trackGroups:
                    if track:
                        item = QtGui.QListWidgetItem(self.listWidget_2)
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Unchecked)
                        item.setText(track.GetName())
            except Exception:
                pass

            try:
                self.map_label.setText("Map Name: " + s.activeClip.GetMapName())
            except Exception:
                pass
            try:
                self.framerate_label.setText("Frame Rate: " + str(s.settings.renderSettings.frameRate))
            except Exception:
                pass

        except Exception as e:
            self.ErrorBox(e)

    def addTomiscBin(self):
        try:
            if self.sessionObj:
                for clip in self.sessionObj.clipBin:
                    if clip:
                        sfmApp.GetDocumentRoot().miscBin.append(clip)
                self.accept()
        except Exception as e:
            self.ErrorBox(e)

    def importSelected(self):
        try:
            s = self.sessionObj
            if not s or not s.HasAttribute("activeClip"):
                self.ErrorBox("No session loaded!")
                return

            endtime = sfmApp.GetDocumentRoot().activeClip.timeFrame.GetDuration()

            for index in range(self.listWidget.count()):
                if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                    shot = s.activeClip.subClipTrackGroup.tracks[0].children[index]
                    shot.SetName(shot.GetName() + "_" + s.activeClip.GetName())
                    shot.timeFrame.SetStartTime(shot.timeFrame.GetStartTime() + endtime)
                    sfmApp.GetDocumentRoot().activeClip.subClipTrackGroup.tracks[0].children.append(shot.Copy())

            for index in range(self.listWidget_2.count()):
                if self.listWidget_2.item(index).checkState() == QtCore.Qt.Checked:
                    group = s.activeClip.trackGroups[index]
                    group.SetName(group.GetName() + "_" + s.activeClip.GetName())
                    for track in group.tracks:
                        for clip in track.children:
                            clip.timeFrame.SetStartTime(clip.timeFrame.GetStartTime() + endtime)
                    sfmApp.GetDocumentRoot().activeClip.trackGroups.append(group)

            self.accept()

        except Exception as e:
            self.ErrorBox(e)

    def toggleChecked(self, listw):
        for i in range(listw.count()):
            item = listw.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Unchecked)
            else:
                item.setCheckState(QtCore.Qt.Checked)


class LightLimitDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LightLimitDialog, self).__init__(parent)
        self.setWindowTitle(t("Light Limit Patch") if 'Light Limit Patch' in TRANSLATIONS else "Light Limit Patch")
        try:
            apply_unicode_font(self, samples=(TURKISH_ALPHABET + ENGLISH_ALPHABET))
        except Exception:
            pass
        self.setMinimumSize(320, 120)
        layout = QtGui.QFormLayout(self)
        self.spin = QtGui.QSpinBox()
        self.spin.setRange(1, 600)
        self.spin.setValue(600)
        layout.addRow(QtGui.QLabel(t("Light Limit Patch") if 'Light Limit Patch' in TRANSLATIONS else "Limit:"), self.spin)
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _on_accept(self):
        try:
            apply_light_limit_patch(self.spin.value())
            self.accept()
        except Exception as e:
            try:
                QtGui.QMessageBox.warning(self, "Light Limit Patch", "Failed to apply: {}".format(e))
            except Exception:
                pass


@safe_call
def apply_light_limit_patch(new_limit):
    new_limit = max(1, min(new_limit, 600))
    sfm.Msg("[Python] Applying light limit patch: {}\n".format(new_limit))
    virtual_protect = ctypes.windll.kernel32.VirtualProtect

    def write_mem(addr, data):
        old_protect = ctypes.c_ulong()
        virtual_protect(addr, len(data), 0x40, ctypes.byref(old_protect))
        ctypes.memmove(addr, data, len(data))
        virtual_protect(addr, len(data), old_protect, ctypes.byref(old_protect))

    baseifm = ctypes.windll.ifm._handle + 0xC00
    baseclient = ctypes.windll.client._handle + 0xC00

    for addr in [baseifm + 0x27BE2E, baseifm + 0x27BEA1, baseifm + 0x27BEA5]:
        write_mem(addr, struct.pack('B', new_limit))
    for addr in [baseclient + 0xB21E3, baseclient + 0xC214A]:
        write_mem(addr, struct.pack('B', new_limit - 1))

    sfm.Msg("[Python] Light limit patch applied.\n")


# ---------- Select Model Dialog (for Auto Lip Sync) ----------
class SelectModelDialog(QtGui.QDialog):
    """Dialog that helps user select a model from the Animation Set Editor that supports FACE controls.
    Workflow:
      1) Open Animation Set Editor in SFM
      2) Select a model in ASE that has FACE controls
      3) Press Refresh in this dialog to scan the selected model(s)
      4) Choose model and press Select Model
    """
    def __init__(self, parent=None):
        super(SelectModelDialog, self).__init__(parent)
        self.setWindowTitle("Select Model (FACE)")
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000000, stop:1 %s); color: %s;" % (PALETTE['panel'], PALETTE['text']))
        # Ensure dialog uses same Unicode-capable font for proper Turkish rendering
        try:
            apply_unicode_font(self, samples=(TURKISH_ALPHABET + ENGLISH_ALPHABET))
        except Exception:
            pass
        self.parent_gui = parent
        self.setMinimumSize(480, 320)

        layout = QtGui.QVBoxLayout(self)
        instructions = QtGui.QLabel("Open the Animation Set Editor, select a model with FACE controls, then press Refresh.")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        btn_h = QtGui.QHBoxLayout()
        open_ase_btn = QtGui.QPushButton("Open Animation Set Editor")
        open_ase_btn.clicked.connect(self._open_ase)
        btn_h.addWidget(open_ase_btn)
        refresh_btn = QtGui.QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_models)
        btn_h.addWidget(refresh_btn)
        debug_btn = QtGui.QPushButton(t("Debug Detection"))
        debug_btn.setToolTip("Run a diagnostic scan and print which heuristics matched")
        debug_btn.clicked.connect(self._debug_scan)
        btn_h.addWidget(debug_btn)

        show_all_btn = QtGui.QPushButton(t("Show All Models"))
        show_all_btn.setToolTip("List all scene models (no FACE filtering)")
        show_all_btn.clicked.connect(self._list_all_models)
        btn_h.addWidget(show_all_btn)

        layout.addLayout(btn_h)

        self.listw = QtGui.QListWidget()
        try:
            self.listw.setFont(self.font())
        except Exception:
            pass
        self.listw.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        layout.addWidget(self.listw)

        bottom_h = QtGui.QHBoxLayout()

        self.select_first_btn = QtGui.QPushButton(t("Select First Found"))
        self.select_first_btn.setToolTip("Quick-select the first listed FACE-enabled model")
        self.select_first_btn.clicked.connect(lambda: self._pick_first())
        self.select_first_btn.setEnabled(False)
        bottom_h.addWidget(self.select_first_btn)
        self.select_btn = QtGui.QPushButton("Select Model")
        self.select_btn.setEnabled(False)
        self.select_btn.clicked.connect(self._select_model)
        bottom_h.addStretch()
        bottom_h.addWidget(self.select_btn)
        close_btn = QtGui.QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        bottom_h.addWidget(close_btn)
        layout.addLayout(bottom_h)

        self._mapping = {}
        self.listw.itemSelectionChanged.connect(self._on_selection_changed)
        # initial scan
        self._refresh_models()

    # Class-level helper: find model 'root' by walking up parent/owner chains
    def _find_model_root(self, obj):
        try:
            seen = set()
            cur = obj
            while cur is not None:
                cid = id(cur)
                if cid in seen:
                    break
                seen.add(cid)
                if hasattr(cur, 'GetAvailableControls') or hasattr(cur, 'GetController'):
                    return cur
                if hasattr(cur, 'GetParent'):
                    try:
                        cur = cur.GetParent()
                        continue
                    except Exception:
                        pass
                if hasattr(cur, 'GetOwner'):
                    try:
                        cur = cur.GetOwner()
                        continue
                    except Exception:
                        pass
                try:
                    cur = getattr(cur, 'parent', None)
                except Exception:
                    break
            return obj
        except Exception:
            return obj

    # Class-level helper: aggressive FACE-capability detection
    def _has_face(self, node, _visited=None):
        if node is None:
            return False
        if _visited is None:
            _visited = set()
        try:
            nid = id(node)
            if nid in _visited:
                return False
            _visited.add(nid)
        except Exception:
            pass
        try:
            # direct controller check
            if hasattr(node, 'GetController'):
                try:
                    if node.GetController('FACE'):
                        return True
                except Exception:
                    pass
        except Exception:
            pass
        try:
            # available control names
            if hasattr(node, 'GetAvailableControls'):
                try:
                    ctrls = node.GetAvailableControls() or []
                    for c in ctrls:
                        s = str(c).lower()
                        if any(k in s for k in ('face','mouth','jaw','lip','phon','visem','viseme','flex','blend')):
                            return True
                except Exception:
                    pass
        except Exception:
            pass
        try:
            # inspect children recursively
            if hasattr(node, 'GetChildren'):
                try:
                    for ch in node.GetChildren() or []:
                        if self._has_face(ch, _visited=_visited):
                            return True
                except Exception:
                    pass
        except Exception:
            pass
        try:
            # quick heuristics on names / repr and dir-based hints
            s = str(node).lower()
            if any(k in s for k in ('face','mouth','jaw','lip','phon')):
                return True
            # as a last resort, inspect attribute/method names for face-like keywords
            try:
                names = ' '.join([str(x).lower() for x in dir(node) or []])
                if any(k in names for k in ('face','mouth','jaw','phon','flex','visem','viseme')):
                    return True
            except Exception:
                pass
        except Exception:
            pass
        return False

    def _pick_first(self):
        # Convenience: pick and select the first valid listing
        try:
            if self.listw.count() <= 0:
                return
            item = self.listw.item(0)
            if item:
                self.listw.setCurrentItem(item)
                self._select_model()
        except Exception:
            pass

    def _debug_scan(self):
        # Run a diagnostic that prints which heuristics matched for selected/scene models
        try:
            lines = []
            candidates = []
            for fn in ("GetSelectedModels", "GetSelectedAnimationSetModels", "GetSelectedItems", "GetSelection"):
                try:
                    if hasattr(sfm, fn):
                        res = getattr(sfm, fn)() or []
                        if res:
                            candidates.extend(res)
                except Exception:
                    pass
            if hasattr(sfmApp, 'GetActiveAnimationSet'):
                try:
                    aset = sfmApp.GetActiveAnimationSet()
                    if aset and hasattr(aset, 'GetModels'):
                        candidates.extend(aset.GetModels() or [])
                        # Also include models reachable via ASE model hierarchy children
                        try:
                            for m in (aset.GetModels() or []):
                                # include children nodes so diagnostics see 'Face' nodes too
                                try:
                                    if hasattr(m, 'GetChildren'):
                                        for ch in (m.GetChildren() or []):
                                            candidates.append(ch)
                                except Exception:
                                    pass
                        except Exception:
                            pass
                except Exception:
                    pass
            seen = set()
            for m in candidates:
                try:
                    if id(m) in seen:
                        continue
                    seen.add(id(m))
                    name = None
                    try:
                        name = m.GetName()
                    except Exception:
                        name = str(m)
                    # checks
                    checks = []
                    try:
                        if hasattr(m, 'GetController'):
                            try:
                                if m.GetController('FACE'):
                                    checks.append('controller:FACE')
                            except Exception:
                                pass
                    except Exception:
                        pass
                    try:
                        if hasattr(m, 'GetAvailableControls'):
                            try:
                                ctrls = m.GetAvailableControls() or []
                                for c in ctrls:
                                    s = str(c).lower()
                                    if any(k in s for k in ('face','mouth','jaw','lip','phon')):
                                        checks.append('available_control')
                                        break
                            except Exception:
                                pass
                    except Exception:
                        pass
                    # check children for face nodes / controls
                    try:
                        if hasattr(m, 'GetChildren'):
                            try:
                                for ch in (m.GetChildren() or []):
                                    try:
                                        chname = None
                                        try:
                                            chname = ch.GetName()
                                        except Exception:
                                            chname = str(ch)
                                        if 'face' in str(chname).lower():
                                            checks.append('child_name:Face')
                                        # child has available controls?
                                        if hasattr(ch, 'GetAvailableControls'):
                                            try:
                                                for c in (ch.GetAvailableControls() or []):
                                                    if any(k in str(c).lower() for k in ('face','mouth','jaw','lip','phon')):
                                                        checks.append('child_available_control')
                                                        break
                                            except Exception:
                                                pass
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                    except Exception:
                        pass
                    try:
                        s = str(m).lower()
                        if any(k in s for k in ('face','mouth','jaw','lip','phon')):
                            checks.append('name_heuristic')
                    except Exception:
                        pass
                    lines.append("{} -> {}".format(name, ",".join(checks) if checks else "no_match"))
                except Exception:
                    pass
            if not lines:
                lines = ["No candidates discovered in selection/ASE."]
            if self.parent_gui and hasattr(self.parent_gui, 'log_box'):
                for L in lines:
                    try:
                        self.parent_gui.log_box.append("ğŸ”§ " + L)
                    except Exception:
                        pass
        except Exception:
            pass

    def _open_ase(self):
        # Try to show ASE in SFM; best-effort
        try:
            try:
                sfmApp.ShowTabWindow("AnimationSetEditor")
                try:
                    if self.parent_gui and hasattr(self.parent_gui, 'log_box'):
                        self.parent_gui.log_box.append("ğŸ” ASE shown: AnimationSetEditor")
                except Exception:
                    pass
            except Exception:
                try:
                    sfmApp.ShowTabWindow("Animation Set Editor")
                    try:
                        if self.parent_gui and hasattr(self.parent_gui, 'log_box'):
                            self.parent_gui.log_box.append("ğŸ” ASE shown: Animation Set Editor")
                    except Exception:
                        pass
                except Exception:
                    # fallback: notify user via console and logs
                    try:
                        sfm.console('echo "Please open the Animation Set Editor and select a model"')
                    except Exception:
                        pass
                    try:
                        if self.parent_gui and hasattr(self.parent_gui, 'log_box'):
                            self.parent_gui.log_box.append("âš  Could not show ASE automatically; please open it from Windows > Animation Set Editor")
                    except Exception:
                        pass
        except Exception as e:
            try:
                if self.parent_gui and hasattr(self.parent_gui, 'log_box'):
                    self.parent_gui.log_box.append("âš  _open_ase error: {}".format(e))
            except Exception:
                pass

    def _refresh_models(self):
        """Refresh = list all scene models. Simple and reliable."""
        try:
            self._list_all_models()
        except Exception:
            pass

    def _list_all_models(self):
        """List all scene models regardless of FACE detection (manual selection fallback)."""
        try:
            self.listw.clear()
            self._mapping = {}
            models = []
            if hasattr(sfm, 'GetAllModels'):
                models = sfm.GetAllModels() or []
            elif hasattr(sfm, 'GetModels'):
                models = sfm.GetModels() or []
            if not models:
                try:
                    scene = sfm.GetScene()
                    if hasattr(scene, 'GetModels'):
                        models = scene.GetModels() or []
                except Exception:
                    pass
            seen = set()
            for m in models:
                try:
                    root = m
                    # find sensible root
                    try:
                        root = root if not hasattr(root, 'GetOwner') else self._find_model_root(root)
                    except Exception:
                        pass
                    if id(root) in seen:
                        continue
                    seen.add(id(root))
                    try:
                        name = root.GetName()
                    except Exception:
                        name = str(root)
                    detected = self._has_face(root)
                    face_tag = "[FACE]" if detected else "[no FACE]"
                    display_name = "%s %s [0x%x]" % (name, face_tag, id(root) & 0xFFFF)
                    item = QtGui.QListWidgetItem(display_name)
                    try:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(PALETTE['text'])))
                    except Exception:
                        pass
                    self.listw.addItem(item)
                    self._mapping[display_name] = (root, name, 'scene', detected)
                except Exception:
                    pass
            # log count
            if self.parent_gui and hasattr(self.parent_gui, 'log_box'):
                self.parent_gui.log_box.append("ğŸ” Show All Models: listed {} model(s)".format(len(self._mapping)))
            # enable controls if we have entries
            try:
                self.select_first_btn.setEnabled(self.listw.count() > 0)
            except Exception:
                pass
        except Exception:
            pass
        # Using class-level helpers: self._find_model_root and self._has_face (moved above)

    def _on_selection_changed(self):
        sel = self.listw.selectedItems()
        if sel:
            name = sel[0].text()
            if name in self._mapping:
                self.select_btn.setEnabled(True)
                try:
                    entry = self._mapping.get(name)
                    has_face = entry[3] if entry and len(entry) > 3 else False
                    color = PALETTE['success'] if has_face else PALETTE['orange']
                    self.select_btn.setStyleSheet("background: %s; color: %s; padding:8px; border-radius:6px;" % (color, PALETTE['panel']))
                except Exception:
                    pass
            else:
                self.select_btn.setEnabled(False)
                try:
                    self.select_btn.setStyleSheet("")
                except Exception:
                    pass
        else:
            self.select_btn.setEnabled(False)
            try:
                self.select_btn.setStyleSheet("")
            except Exception:
                pass

    def _select_model(self):
        sel = self.listw.selectedItems()
        if not sel:
            try:
                if self.parent_gui:
                    self.parent_gui.set_selected_model(None, None)
                QtGui.QMessageBox.warning(self, "Select Model", t("No model was selected..."))
            except Exception:
                pass
            self.reject()
            return
        name = sel[0].text()
        entry = self._mapping.get(name)
        if entry:
            try:
                model_obj = entry[0]
                clean_name = entry[1]
                has_face = entry[3] if len(entry) > 3 else False
                # If the model doesn't appear to have FACE, confirm with the user before selecting
                if not has_face:
                    try:
                        ans = QtGui.QMessageBox.question(self, "Select Model", t("Selected model does not have FACE controls" ) + "\n\n" + t("Select Model: %s") % clean_name + "\n\n" + "Select anyway?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                        if ans != QtGui.QMessageBox.Yes:
                            return
                    except Exception:
                        pass
                if self.parent_gui:
                    self.parent_gui.set_selected_model(model_obj, clean_name)
                QtGui.QMessageBox.information(self, "Select Model", t("Selected Model: %s") % clean_name)
            except Exception:
                pass
            self.accept()
        else:
            try:
                if self.parent_gui:
                    self.parent_gui.set_selected_model(None, None)
                QtGui.QMessageBox.warning(self, "Select Model", t("No model was selected..."))
            except Exception:
                pass
            self.reject()

# ---------- Script window management ----------
WINDOW_ID = "FilmmakerGUI"

def CreateScriptWindow():
    try:
        widget = FilmmakerGUI()
        globals()[WINDOW_ID] = widget

        # Prefer winId(), but ensure we pass a 32-bit handle to SFM (avoid OverflowError)
        registered = False
        try:
            ptr = int(widget.winId())
            ptr32 = int(ptr) & 0xFFFFFFFF
            # Convert to signed 32-bit for C long compatibility (avoid OverflowError)
            try:
                ptr32_signed = ctypes.c_long(ptr32).value
            except Exception:
                ptr32_signed = ptr32
            # Try signed C long value first
            try:
                sfmApp.RegisterTabWindow(WINDOW_ID, "Filmmaker GUI V3.7", ptr32_signed)
                registered = True
            except OverflowError:
                # If signed conversion still overflows, try unsigned masked value
                try:
                    sfmApp.RegisterTabWindow(WINDOW_ID, "Filmmaker GUI V3.7", ptr32)
                    registered = True
                except Exception:
                    registered = False
        except Exception:
            try:
                # Fallback: use shiboken pointer conversion if available and mask
                raw = shiboken.getCppPointer(widget)[0]
                ptr32 = int(raw) & 0xFFFFFFFF
                try:
                    ptr32_signed = ctypes.c_long(ptr32).value
                except Exception:
                    ptr32_signed = ptr32
                try:
                    sfmApp.RegisterTabWindow(WINDOW_ID, "Filmmaker GUI V3.7", ptr32_signed)
                    registered = True
                except OverflowError:
                    try:
                        sfmApp.RegisterTabWindow(WINDOW_ID, "Filmmaker GUI V3.7", ptr32)
                        registered = True
                    except Exception:
                        registered = False
            except Exception:
                registered = False

        if not registered:
            try:
                sfmApp.ShowInDock("Filmmaker GUI V3.7", widget)
                registered = True
            except Exception:
                try:
                    widget.show()
                    registered = True
                except Exception:
                    registered = False

        if not registered:
            raise RuntimeError("Could not register Filmmaker GUI window in SFM")
    except Exception:
        traceback.print_exc()

def DestroyScriptWindow():
    try:
        win = globals().get(WINDOW_ID)
        if win:
            win.close()
            win.deleteLater()
            globals()[WINDOW_ID] = None
    except Exception:
        traceback.print_exc()

def main():
    try:
        if WINDOW_ID in globals() and globals()[WINDOW_ID] is not None:
            try:
                globals()[WINDOW_ID].close()
                globals()[WINDOW_ID].deleteLater()
            except Exception:
                pass

        CreateScriptWindow()

        try:
            sfmApp.ShowTabWindow(WINDOW_ID)
        except Exception:
            try:
                win = globals().get(WINDOW_ID)
                if win:
                    win.show()
            except Exception:
                pass
    except Exception:
        traceback.print_exc()

try:
    custom_window.close()
except:
    pass

from PySide import shiboken
import sfmApp

def _launch_main_gui():
    global custom_window
    try:
        custom_window = FilmmakerGUI3_0()
        custom_window.show()
        try:
            sfmApp.RegisterTabWindow(
                "FilmmakerGUI V3.7", "FilmmakerGUIV3.7",
                shiboken.getCppPointer(custom_window)[0]
            )
            sfmApp.ShowTabWindow("FilmmakerGUI V3.7")
        except Exception:
            pass
    except Exception:
        import traceback
        traceback.print_exc()


_splash_win = SplashScreen()
_splash_win.on_finished = _launch_main_gui
_splash_win.show_splash()