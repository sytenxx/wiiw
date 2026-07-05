#!/usr/bin/env python3
# ============================================================
# HIRAKOX TOOLKIT v3.0 - TELEGRAM BOT
# Features: BIN Lookup | CC Generator | Fake User | CC Checker | BIN Database
# Telegram: @hirakox
# ============================================================

import requests
from bs4 import BeautifulSoup
import json
import sys
import re
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from io import BytesIO
import asyncio

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram imports
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("[!] Please install python-telegram-bot: pip install python-telegram-bot")
    sys.exit(1)

# ============================================================
# KONFIGURASI BOT
# ============================================================
BOT_TOKEN = "8892880847:AAGr5YURMe9EXmA4iXi9cxaYwKr-t5ZTzAs"

# ============================================================
# KONFIGURASI
# ============================================================
VENDOR_LIST = ['Visa', 'MASTERCARD', 'AMERICAN EXPRESS', 'Maestro', 'Discover', 'DCI', 'JCB', 'CHINA UNION PAY']
LEVEL_LIST = ['Classic/Standard', 'Gold/Prem', 'Platinum', 'Signature', 'Electron', 'Prepaid', 'Business', 'Corporate', 'Infinite', 'Cash', 'Purchasing', 'Virtual']
TYPE_LIST = ['Credit', 'Debit', 'CHARGE CARD', 'unknown']

LANG = 'en'

# ============================================================
# TRANSLATIONS
# ============================================================
def t(key):
    texts = {
        'en': {
            'menu_title': "MAIN MENU",
            'menu_1': "1. BIN Lookup (Search/Validate)",
            'menu_2': "2. Generate Credit Cards ",
            'menu_3': "3. Generate Fake Users",
            'menu_4': "4. CC Checker (Validate Cards)",
            'menu_5': "5. About",
            'menu_6': "6. Exit",
            'menu_choice': "Choose [1-6]: ",
            'bin_menu': "BIN LOOKUP",
            'input_mode': "INPUT MODE",
            'input_1': "1. Manual (space/comma separated)",
            'input_2': "2. Read from file",
            'input_3': "3. Generate + Validate (suffix 1-9)",
            'input_choice': "Choose [1-3]: ",
            'filename': "Filename: ",
            'manual_input': "Enter BINs (space/comma): ",
            'invalid_bin': "[!] No valid BIN found.",
            'file_not_found': "[!] File '{0}' not found.",
            'loaded': "[+] Loaded {0} BINs from {1}",
            'filter_title': "FILTER OPTIONS (0 to skip and comma for many choices)",
            'select_vendor': "Select VENDOR:",
            'select_level': "Select LEVEL:",
            'select_type': "Select TYPE:",
            'country_prompt': "Country (2 letters, e.g. US): ",
            'bank_prompt': "Bank name (partial): ",
            'searching': "[*] Searching {0} BINs ...",
            'validating': "[*] Validating {0} BINs ...",
            'no_results': "[-] No results from server.",
            'try_no_filter': "[*] Try without filters.",
            'results_found': "[+] Found {0} results:",
            'saved': "[+] Saved to {0}",
            'generate_title': "GENERATE + VALIDATE",
            'suffix_prompt': "Enter suffix (1-9): ",
            'suffix_invalid': "[!] Suffix must be 1-9!",
            'count_prompt': "How many to generate? (default: 10): ",
            'generated': "[+] Generated {0} BINs:",
            'validate_ask': "Validate to web? (y/n): ",
            'save_ask': "Save to file? (y/n): ",
            'save_filename': "Filename (default: generated.txt): ",
            'saved_generated': "[+] Saved to {0}",
            'error': "[!] Error: {0}",
            'debug': "[DEBUG] HTML:",
            'bin': "BIN",
            'country': "Country",
            'vendor': "Vendor",
            'type': "Type",
            'level': "Level",
            'bank': "Bank",
            'skip': "skip",
            'exit': "Exiting... Goodbye!",
            'checker_title': "CC CHECKER",
            'checker_mode': "Check mode:",
            'checker_1': "1. Single Check",
            'checker_2': "2. Bulk Check (from file)",
            'checker_3': "3. Bulk Check (manual input)",
            'checker_choice': "Choose [1-3]: ",
            'checking': "[*] Checking {0} cards...",
            'export_mode': "Export mode:",
            'export_1': "1. Full Report (with details)",
            'export_2': "2. LIVE Cards Only (format: number|mm|yy|cvv)",
            'export_choice': "Choose [1/2]: ",
            'saved_live': "[+] {0} LIVE cards saved to {1}",
        },
        'id': {
            'menu_title': "MENU UTAMA",
            'menu_1': "1. Cari BIN (Lookup/Validasi)",
            'menu_2': "2. Generate Kartu Kredit",
            'menu_3': "3. Generate User Palsu",
            'menu_4': "4. CC Checker (Validasi Kartu)",
            'menu_5': "5. Tentang",
            'menu_6': "6. Keluar",
            'menu_choice': "Pilih [1-6]: ",
            'bin_menu': "BIN LOOKUP",
            'input_mode': "MODE INPUT",
            'input_1': "1. Manual (pisah spasi/koma)",
            'input_2': "2. Baca dari file",
            'input_3': "3. Generate + Validasi (suffix 1-9)",
            'input_choice': "Pilih [1-3]: ",
            'filename': "Nama file: ",
            'manual_input': "Masukkan BIN (spasi/koma): ",
            'invalid_bin': "[!] Ga ada BIN valid.",
            'file_not_found': "[!] File '{0}' ga ketemu.",
            'loaded': "[+] Load {0} BIN dari {1}",
            'filter_title': "FILTER OPSI (0 untuk lewati dan comma untuk banyak pilihan)",
            'select_vendor': "Pilih VENDOR:",
            'select_level': "Pilih LEVEL:",
            'select_type': "Pilih TYPE:",
            'country_prompt': "Country (2 huruf, contoh: US): ",
            'bank_prompt': "Nama bank (partial): ",
            'searching': "[*] Mencari {0} BIN ...",
            'validating': "[*] Validasi {0} BIN ...",
            'no_results': "[-] Ga ada hasil dari server.",
            'try_no_filter': "[*] Coba tanpa filter.",
            'results_found': "[+] Ditemukan {0} hasil:",
            'saved': "[+] Disimpan ke {0}",
            'generate_title': "GENERATE + VALIDASI",
            'suffix_prompt': "Masukkan suffix (1-9): ",
            'suffix_invalid': "[!] Suffix harus 1-9!",
            'count_prompt': "Mau generate berapa? (default: 10): ",
            'generated': "[+] Generate {0} BIN:",
            'validate_ask': "Validasi ke web? (y/n): ",
            'save_ask': "Simpan ke file? (y/n): ",
            'save_filename': "Nama file (default: generated.txt): ",
            'saved_generated': "[+] Disimpan ke {0}",
            'error': "[!] Error: {0}",
            'debug': "[DEBUG] HTML:",
            'bin': "BIN",
            'country': "Country",
            'vendor': "Vendor",
            'type': "Type",
            'level': "Level",
            'bank': "Bank",
            'skip': "lewati",
            'exit': "Keluar... Sampai jumpa!",
            'checker_title': "CC CHECKER",
            'checker_mode': "Mode cek:",
            'checker_1': "1. Cek Satu",
            'checker_2': "2. Cek Banyak (dari file)",
            'checker_3': "3. Cek Banyak (input manual)",
            'checker_choice': "Pilih [1-3]: ",
            'checking': "[*] Mengecek {0} kartu...",
            'export_mode': "Mode export:",
            'export_1': "1. Full Report (dengan detail)",
            'export_2': "2. Hanya Kartu LIVE (format: number|mm|yy|cvv)",
            'export_choice': "Pilih [1/2]: ",
            'saved_live': "[+] {0} kartu LIVE disimpan ke {1}",
        }
    }
    return texts[LANG].get(key, key)

# ============================================================
# BIN DATABASE CLASS
# ============================================================
class BINDatabase:
    def __init__(self):
        self.country_urls = {
            "indonesia": "https://www.freebinchecker.com/indonesia-bin-list",
            "usa": "https://www.freebinchecker.com/usa-bin-list",
            "uk": "https://www.freebinchecker.com/united-kingdom-bin-list",
            "singapore": "https://www.freebinchecker.com/singapore-bin-list",
            "malaysia": "https://www.freebinchecker.com/malaysia-bin-list",
            "australia": "https://www.freebinchecker.com/australia-bin-list",
            "canada": "https://www.freebinchecker.com/canada-bin-list",
            "germany": "https://www.freebinchecker.com/germany-bin-list",
            "france": "https://www.freebinchecker.com/france-bin-list",
            "netherlands": "https://www.freebinchecker.com/netherlands-bin-list",
            "spain": "https://www.freebinchecker.com/spain-bin-list",
            "italy": "https://www.freebinchecker.com/italy-bin-list",
            "brazil": "https://www.freebinchecker.com/brazil-bin-list",
            "mexico": "https://www.freebinchecker.com/mexico-bin-list",
            "argentina": "https://www.freebinchecker.com/argentina-bin-list",
            "chile": "https://www.freebinchecker.com/chile-bin-list",
            "colombia": "https://www.freebinchecker.com/colombia-bin-list",
            "peru": "https://www.freebinchecker.com/peru-bin-list",
            "venezuela": "https://www.freebinchecker.com/venezuela-bin-list",
            "south-africa": "https://www.freebinchecker.com/south-africa-bin-list",
            "egypt": "https://www.freebinchecker.com/egypt-bin-list",
            "nigeria": "https://www.freebinchecker.com/nigeria-bin-list",
            "kenya": "https://www.freebinchecker.com/kenya-bin-list",
            "pakistan": "https://www.freebinchecker.com/pakistan-bin-list",
            "india": "https://www.freebinchecker.com/india-bin-list",
            "philippines": "https://www.freebinchecker.com/philippines-bin-list",
            "thailand": "https://www.freebinchecker.com/thailand-bin-list",
            "vietnam": "https://www.freebinchecker.com/vietnam-bin-list",
            "south-korea": "https://www.freebinchecker.com/south-korea-bin-list",
            "japan": "https://www.freebinchecker.com/japan-bin-list",
            "china": "https://www.freebinchecker.com/china-bin-list",
            "hong-kong": "https://www.freebinchecker.com/hong-kong-bin-list",
            "taiwan": "https://www.freebinchecker.com/taiwan-bin-list",
            "new-zealand": "https://www.freebinchecker.com/new-zealand-bin-list",
            "russia": "https://www.freebinchecker.com/russia-bin-list",
            "turkey": "https://www.freebinchecker.com/turkey-bin-list",
            "saudi-arabia": "https://www.freebinchecker.com/saudi-arabia-bin-list",
            "uae": "https://www.freebinchecker.com/uae-bin-list",
            "israel": "https://www.freebinchecker.com/israel-bin-list",
            "poland": "https://www.freebinchecker.com/poland-bin-list",
            "sweden": "https://www.freebinchecker.com/sweden-bin-list",
            "norway": "https://www.freebinchecker.com/norway-bin-list",
            "denmark": "https://www.freebinchecker.com/denmark-bin-list",
            "finland": "https://www.freebinchecker.com/finland-bin-list",
            "ireland": "https://www.freebinchecker.com/ireland-bin-list",
            "portugal": "https://www.freebinchecker.com/portugal-bin-list",
            "greece": "https://www.freebinchecker.com/greece-bin-list",
            "czech-republic": "https://www.freebinchecker.com/czech-republic-bin-list",
            "hungary": "https://www.freebinchecker.com/hungary-bin-list",
            "romania": "https://www.freebinchecker.com/romania-bin-list",
            "ukraine": "https://www.freebinchecker.com/ukraine-bin-list",
            "kazakhstan": "https://www.freebinchecker.com/kazakhstan-bin-list",
            "uzbekistan": "https://www.freebinchecker.com/uzbekistan-bin-list",
            "bangladesh": "https://www.freebinchecker.com/bangladesh-bin-list",
            "sri-lanka": "https://www.freebinchecker.com/sri-lanka-bin-list",
            "nepal": "https://www.freebinchecker.com/nepal-bin-list",
            "myanmar": "https://www.freebinchecker.com/myanmar-bin-list",
            "cambodia": "https://www.freebinchecker.com/cambodia-bin-list",
            "laos": "https://www.freebinchecker.com/laos-bin-list",
            "brunei": "https://www.freebinchecker.com/brunei-bin-list",
            "timor-leste": "https://www.freebinchecker.com/timor-leste-bin-list",
            "papua-new-guinea": "https://www.freebinchecker.com/papua-new-guinea-bin-list",
            "fiji": "https://www.freebinchecker.com/fiji-bin-list",
            "morocco": "https://www.freebinchecker.com/morocco-bin-list",
            "algeria": "https://www.freebinchecker.com/algeria-bin-list",
            "tunisia": "https://www.freebinchecker.com/tunisia-bin-list",
            "ghana": "https://www.freebinchecker.com/ghana-bin-list",
            "angola": "https://www.freebinchecker.com/angola-bin-list",
            "ethiopia": "https://www.freebinchecker.com/ethiopia-bin-list",
            "tanzania": "https://www.freebinchecker.com/tanzania-bin-list",
            "uganda": "https://www.freebinchecker.com/uganda-bin-list",
            "zimbabwe": "https://www.freebinchecker.com/zimbabwe-bin-list",
            "botswana": "https://www.freebinchecker.com/botswana-bin-list",
            "namibia": "https://www.freebinchecker.com/namibia-bin-list",
            "mauritius": "https://www.freebinchecker.com/mauritius-bin-list",
            "seychelles": "https://www.freebinchecker.com/seychelles-bin-list",
        }
        
        self.regions = {
            "asia": ["indonesia", "singapore", "malaysia", "philippines", "thailand", 
                     "vietnam", "india", "pakistan", "china", "japan", "south-korea", 
                     "hong-kong", "taiwan", "israel", "uae", "saudi-arabia", 
                     "bangladesh", "sri-lanka", "nepal", "myanmar", "cambodia", 
                     "laos", "brunei", "timor-leste", "kazakhstan", "uzbekistan"],
            
            "europe": ["uk", "germany", "france", "netherlands", "spain", "italy", 
                       "russia", "turkey", "poland", "sweden", "norway", "denmark", 
                       "finland", "ireland", "portugal", "greece", "czech-republic", 
                       "hungary", "romania", "ukraine"],
            
            "america": ["usa", "canada", "brazil", "mexico", "argentina", "chile", 
                        "colombia", "peru", "venezuela"],
            
            "africa": ["south-africa", "egypt", "nigeria", "kenya", "morocco", 
                       "algeria", "tunisia", "ghana", "angola", "ethiopia", 
                       "tanzania", "uganda", "zimbabwe", "botswana", "namibia", 
                       "mauritius", "seychelles"],
            
            "oceania": ["australia", "new-zealand", "papua-new-guinea", "fiji"]
        }
    
    def scrape_bins(self, country, limit=None):
        """Scrape BIN dari website dengan limit jumlah"""
        if country not in self.country_urls:
            return []
        
        url = self.country_urls[country]
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            return []
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        bins = []
        
        tables = soup.find_all("table", class_="table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    bin_cell = cols[0]
                    link = bin_cell.find("a")
                    bin_num = link.get_text(strip=True) if link else bin_cell.get_text(strip=True)
                    
                    if re.match(r'^\d{6,8}$', bin_num):
                        bins.append({
                            "BIN": bin_num,
                            "Network": cols[1].get_text(strip=True).upper(),
                            "Card Type": cols[2].get_text(strip=True).lower(),
                            "Level": cols[3].get_text(strip=True).upper(),
                            "Country": country.title()
                        })
        
        # Hapus duplikat
        seen = set()
        unique = []
        for b in bins:
            key = b["BIN"]
            if key not in seen:
                seen.add(key)
                unique.append(b)
        
        # Batasi jumlah jika diminta
        if limit and limit > 0:
            unique = unique[:limit]
        
        return unique
    
    def get_bin_detail(self, bin_num):
        """Scrape detail BIN dari freebinchecker.com/bin-lookup/"""
        url = f"https://www.freebinchecker.com/bin-lookup/{bin_num}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
        except Exception:
            return None
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        card_info = {
            "BIN": bin_num,
            "Network": "N/A",
            "Card Type": "N/A",
            "Level": "N/A",
            "Bank": "N/A",
            "Country": "N/A",
            "Country Code": "N/A"
        }
        
        tables = soup.find_all("table", class_="table")
        
        # Ambil Card Information
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    header = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    
                    if "IIN / BIN" in header:
                        card_info["BIN"] = value
                    elif "Network Company" in header:
                        card_info["Network"] = value.upper()
                    elif "Card Type" in header:
                        card_info["Card Type"] = value.lower()
                    elif "Card Level" in header:
                        card_info["Level"] = value.upper()
        
        # Ambil Bank
        for table in tables:
            thead = table.find("thead")
            if thead:
                header_text = thead.get_text(strip=True).lower()
                if "name" in header_text and "website" in header_text:
                    rows = table.find_all("tr")
                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            bank_name = cols[0].get_text(strip=True)
                            if bank_name and bank_name not in ["Name", "Website", "Phone", "City"]:
                                card_info["Bank"] = bank_name
                                break
        
        # Ambil Country
        for table in tables:
            thead = table.find("thead")
            if thead:
                header_text = thead.get_text(strip=True).lower()
                if "flag" in header_text and "code" in header_text:
                    rows = table.find_all("tr")
                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) >= 3:
                            country = cols[2].get_text(strip=True)
                            code = cols[1].get_text(strip=True)
                            if country and country not in ["Name", "Code", "Numeric"]:
                                card_info["Country"] = country
                                card_info["Country Code"] = code
                                break
        
        return card_info
    
    def get_all_countries(self):
        return sorted(self.country_urls.keys())
    
    def get_countries_by_region(self, region):
        return self.regions.get(region.lower(), [])

# ============================================================
# BIN LOOKUP FUNCTIONS
# ============================================================
def search_bin(bin_list, filters=None):
    url = "https://bins.su/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "action": "searchbins",
        "bins": "\n".join(bin_list),
        "bank": "",
        "country": ""
    }
    
    if filters:
        data['vendor[]'] = filters.get('vendor', [])
        data['level[]'] = filters.get('level', [])
        data['type[]'] = filters.get('type', [])
        data['bank'] = filters.get('bank', '')
        data['country'] = filters.get('country', '')
    
    try:
        resp = requests.post(url, data=data, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"Error: {e}"

def parse_bin_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    result_div = soup.find('div', id='result')
    if not result_div:
        return results
    
    for table in result_div.find_all('table'):
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 6:
                bin_num = cols[0].get_text(strip=True)
                if not re.match(r'^\d{6,}$', bin_num):
                    continue
                results.append({
                    "bin": bin_num,
                    "country": cols[1].get_text(strip=True),
                    "vendor": cols[2].get_text(strip=True),
                    "type": cols[3].get_text(strip=True),
                    "level": cols[4].get_text(strip=True),
                    "bank": cols[5].get_text(strip=True)
                })
    return results

# ============================================================
# CC GENERATOR FUNCTIONS
# ============================================================
CARD_TYPES = {
    'visa': {'prefix': ['4'], 'length': 16, 'name': 'Visa'},
    'mastercard': {'prefix': ['51', '52', '53', '54', '55', '2221', '2222', '2223', '2224', '2225', '2226', '2227', '2228', '2229', '2230', '2231', '2232', '2233', '2234', '2235', '2236', '2237', '2238', '2239', '2240', '2241', '2242', '2243', '2244', '2245', '2246', '2247', '2248', '2249', '2250', '2251', '2252', '2253', '2254', '2255', '2256', '2257', '2258', '2259', '2260', '2261', '2262', '2263', '2264', '2265', '2266', '2267', '2268', '2269', '2270', '2271', '2272', '2273', '2274', '2275', '2276', '2277', '2278', '2279', '2280', '2281', '2282', '2283', '2284', '2285', '2286', '2287', '2288', '2289', '2290', '2291', '2292', '2293', '2294', '2295', '2296', '2297', '2298', '2299', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50'], 'length': 16, 'name': 'Mastercard'},
    'amex': {'prefix': ['34', '37'], 'length': 15, 'name': 'American Express'},
    'discover': {'prefix': ['6011', '644', '645', '646', '647', '648', '649', '65'], 'length': 16, 'name': 'Discover'},
    'diners': {'prefix': ['300', '301', '302', '303', '304', '305', '36', '38', '39'], 'length': 14, 'name': 'Diners Club'},
    'jcb': {'prefix': ['3528', '3529', '3530', '3531', '3532', '3533', '3534', '3535', '3536', '3537', '3538', '3539', '3540', '3541', '3542', '3543', '3544', '3545', '3546', '3547', '3548', '3549', '3550', '3551', '3552', '3553', '3554', '3555', '3556', '3557', '3558', '3559', '3560', '3561', '3562', '3563', '3564', '3565', '3566', '3567', '3568', '3569', '3570', '3571', '3572', '3573', '3574', '3575', '3576', '3577', '3578', '3579', '3580', '3581', '3582', '3583', '3584', '3585', '3586', '3587', '3588', '3589', '3590', '3591', '3592', '3593', '3594', '3595', '3596', '3597', '3598', '3599'], 'length': 16, 'name': 'JCB'},
    'maestro': {'prefix': ['50', '56', '57', '58', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70'], 'length': 16, 'name': 'Maestro'},
    'unionpay': {'prefix': ['62', '81'], 'length': 16, 'name': 'UnionPay'},
}

def detect_card_type(bin_prefix: str) -> str:
    bin_prefix = str(bin_prefix)
    for card_type, config in CARD_TYPES.items():
        for prefix in config['prefix']:
            if bin_prefix.startswith(prefix):
                return card_type
    return 'visa'

def calculate_luhn_check_digit(number: str) -> int:
    digits = [int(d) for d in number]
    total = 0
    is_even = True
    
    for i in range(len(digits) - 1, -1, -1):
        digit = digits[i]
        if is_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
        is_even = not is_even
    
    return (10 - (total % 10)) % 10

def validate_luhn(number: str) -> bool:
    digits = [int(d) for d in number]
    total = 0
    is_even = False
    
    for i in range(len(digits) - 1, -1, -1):
        digit = digits[i]
        if is_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
        is_even = not is_even
    
    return total % 10 == 0

def generate_single_card(bin_input: str = '', card_type: str = 'auto', 
                         month: str = '', year: str = '', cvv_mode: str = 'random') -> Optional[Dict]:
    if card_type == 'auto' and bin_input:
        selected_type = detect_card_type(bin_input)
    elif card_type != 'auto':
        selected_type = card_type
    else:
        selected_type = random.choice(list(CARD_TYPES.keys()))
    
    type_config = CARD_TYPES.get(selected_type)
    if not type_config:
        return None
    
    target_length = type_config['length']
    card_number = ''
    
    if bin_input and len(bin_input) > 0:
        card_number = bin_input[:min(len(bin_input), target_length - 1)]
        if len(card_number) > target_length - 1:
            card_number = card_number[:target_length - 1]
    else:
        card_number = random.choice(type_config['prefix'])
    
    while len(card_number) < target_length - 1:
        card_number += str(random.randint(0, 9))
    
    check_digit = calculate_luhn_check_digit(card_number)
    card_number += str(check_digit)
    
    if month.lower() == 'random' or month == '':
        exp_month = str(random.randint(1, 12)).zfill(2)
    else:
        exp_month = str(month).zfill(2)
    
    if year.lower() == 'random' or year == '':
        exp_year = str(random.randint(2026, 2034))
    else:
        exp_year = str(year)
    
    if cvv_mode == 'random':
        card_cvv = ''.join(str(random.randint(0, 9)) for _ in range(3))
    elif cvv_mode == '3digit':
        card_cvv = ''.join(str(random.randint(0, 9)) for _ in range(3))
    elif cvv_mode == '4digit':
        card_cvv = ''.join(str(random.randint(0, 9)) for _ in range(4))
    else:
        card_cvv = ''.join(str(random.randint(0, 9)) for _ in range(3))
    
    return {
        'number': card_number,
        'type': selected_type,
        'type_name': type_config['name'],
        'month': exp_month,
        'year': exp_year,
        'cvv': card_cvv,
        'is_valid': validate_luhn(card_number)
    }

def generate_cards(bin_input: str = '', card_type: str = 'auto', quantity: int = 10,
                   month: str = '', year: str = '', cvv_mode: str = 'random',
                   format_type: str = 'pipe') -> Tuple[List[Dict], int]:
    cards = []
    valid_count = 0
    
    for _ in range(quantity):
        card = generate_single_card(bin_input, card_type, month, year, cvv_mode)
        if card:
            if card['is_valid']:
                valid_count += 1
            
            if format_type == 'pipe':
                card['formatted'] = f"{card['number']}|{card['month']}|{card['year']}|{card['cvv']}"
            elif format_type == 'csv':
                card['formatted'] = f"{card['number']},{card['month']},{card['year']},{card['cvv']}"
            elif format_type == 'sql':
                card['formatted'] = f"INSERT INTO cards (number, month, year, cvv) VALUES ('{card['number']}', '{card['month']}', '{card['year']}', '{card['cvv']}');"
            elif format_type == 'xml':
                card['formatted'] = f"<card><number>{card['number']}</number><month>{card['month']}</month><year>{card['year']}</year><cvv>{card['cvv']}</cvv></card>"
            elif format_type == 'json':
                card['formatted'] = card
            else:
                card['formatted'] = f"{card['number']}|{card['month']}|{card['year']}|{card['cvv']}"
            
            cards.append(card)
    
    return cards, valid_count

def generate_bins_with_suffix(suffix: str, count: int) -> List[str]:
    bin_list = []
    for _ in range(count):
        bin_list.append(f"{suffix}{random.randint(10000, 99999)}")
    return bin_list

# ============================================================
# USER GENERATOR
# ============================================================
def fetch_random_user(gender: str = 'random', nationality: str = 'US') -> Optional[Dict]:
    try:
        params = {}
        if gender != 'random':
            params['gender'] = gender
        params['nat'] = nationality
        
        response = requests.get("https://randomuser.me/api/", params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('results'):
            user = data['results'][0]
            return {
                'name': f"{user['name']['first']} {user['name']['last']}",
                'email': user['email'],
                'phone': user['phone'],
                'address': f"{user['location']['street']['number']} {user['location']['street']['name']}, {user['location']['city']}, {user['location']['state']} {user['location']['postcode']}",
                'country': user['location']['country'],
                'dob': datetime.fromisoformat(user['dob']['date'].replace('Z', '+00:00')).strftime('%Y-%m-%d'),
                'gender': user['gender']
            }
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return None
    return None

def generate_users(quantity: int = 5, gender: str = 'random', nationality: str = 'US') -> List[Dict]:
    users = []
    for _ in range(quantity):
        user = fetch_random_user(gender, nationality)
        if user:
            users.append(user)
        time.sleep(0.3)
    return users

# ============================================================
# CC CHECKER
# ============================================================
def check_card_netverse(card_data: str) -> dict:
    url = "https://netverse.eu.org/api.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Origin": "https://netverse.eu.org",
        "Referer": "https://netverse.eu.org/"
    }
    payload = {"data": card_data}
    
    try:
        resp = requests.post(url, data=payload, headers=headers, timeout=15)
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}", "code": -1}
        try:
            return resp.json()
        except:
            return {"error": "Invalid JSON", "raw": resp.text[:200], "code": -1}
    except Exception as e:
        return {"error": str(e), "code": -1}

def parse_card_netverse(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r'\[(\d+)\]', r'\1', raw)
    raw = raw.replace(" ", "|")
    parts = [p for p in raw.split('|') if p.strip()]
    
    if len(parts) >= 3:
        number = re.sub(r'\s+', '', parts[0])
        month = parts[1].strip().zfill(2)
        year = parts[2].strip()
        if len(year) == 4:
            year = year[2:]
        if len(year) > 2:
            year = year[-2:]
        cvv = parts[3].strip() if len(parts) > 3 else "000"
        
        if number.isdigit() and 13 <= len(number) <= 19:
            if month.isdigit() and 1 <= int(month) <= 12:
                if year.isdigit() and len(year) == 2:
                    return f"{number}|{month}|{year}|{cvv}"
    return None

# ============================================================
# MENU KEYBOARD
# ============================================================
def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🔍 BIN Lookup", callback_data="bin"),
            InlineKeyboardButton("🔢 Gen BIN + Valid", callback_data="genbin")
        ],
        [
            InlineKeyboardButton("💳 CC Generator", callback_data="generate"),
            InlineKeyboardButton("👤 Fake User", callback_data="user")
        ],
        [
            InlineKeyboardButton("✅ CC Checker", callback_data="checker"),
            InlineKeyboardButton("📊 BIN Database", callback_data="bindb")
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================
# CC GENERATOR SETTINGS
# ============================================================
async def cc_generator_settings_callback(query, context):
    keyboard = [
        [
            InlineKeyboardButton("📅 Bulan", callback_data="cc_month"),
            InlineKeyboardButton("📆 Tahun", callback_data="cc_year")
        ],
        [
            InlineKeyboardButton("🔢 CVV", callback_data="cc_cvv"),
            InlineKeyboardButton("📊 Jumlah", callback_data="cc_quantity")
        ],
        [
            InlineKeyboardButton("✅ Generate Sekarang", callback_data="cc_generate_now"),
            InlineKeyboardButton("🔙 Kembali", callback_data="cc_settings_back")
        ]
    ]
    
    month = context.user_data.get('cc_month', 'random')
    year = context.user_data.get('cc_year', 'random')
    cvv = context.user_data.get('cc_cvv', 'random')
    quantity = context.user_data.get('cc_quantity', 10)
    
    cvv_names = {
        'random': 'Random (3 digit)',
        '3digit': '3 Digit',
        '4digit': '4 Digit'
    }
    cvv_display = cvv_names.get(cvv, cvv)
    
    settings_text = f"""
⚙️ *CC GENERATOR SETTINGS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *Pengaturan Saat Ini:*

• 📅 Bulan: `{month}`
• 📆 Tahun: `{year}`
• 🔢 CVV: `{cvv_display}`
• 📊 Jumlah: `{quantity}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Pilih pengaturan di bawah:
"""
    await query.edit_message_text(
        settings_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def cc_month_menu_callback(query, context):
    months = [
        ["Jan", "Feb", "Mar", "Apr"],
        ["May", "Jun", "Jul", "Aug"],
        ["Sep", "Oct", "Nov", "Dec"]
    ]
    
    keyboard = []
    for row in months:
        buttons = []
        for m in row:
            buttons.append(InlineKeyboardButton(m, callback_data=f"cc_month_{m[:3].lower()}"))
        keyboard.append(buttons)
    
    keyboard.append([InlineKeyboardButton("🎲 Random", callback_data="cc_month_random")])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="cc_settings")])
    
    await query.edit_message_text(
        "📅 *Pilih Bulan Expiry*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Pilih bulan untuk kartu yang digenerate:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def cc_year_menu_callback(query, context):
    current_year = datetime.now().year
    years = []
    for i in range(8):
        years.append(str(current_year + i))
    
    keyboard = []
    row = []
    for y in years:
        row.append(InlineKeyboardButton(y, callback_data=f"cc_year_{y}"))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🎲 Random", callback_data="cc_year_random")])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="cc_settings")])
    
    await query.edit_message_text(
        "📆 *Pilih Tahun Expiry*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Pilih tahun untuk kartu yang digenerate:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def cc_cvv_menu_callback(query, context):
    keyboard = [
        [InlineKeyboardButton("🎲 Random (3 digit)", callback_data="cc_cvv_random")],
        [InlineKeyboardButton("🔢 3 Digit", callback_data="cc_cvv_3digit")],
        [InlineKeyboardButton("🔢 4 Digit (AMEX)", callback_data="cc_cvv_4digit")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="cc_settings")]
    ]
    
    await query.edit_message_text(
        "🔢 *Pilih CVV*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Pilih jenis CVV untuk kartu:\n"
        "• Random - CVV acak 3 digit\n"
        "• 3 Digit - CVV 3 digit\n"
        "• 4 Digit - CVV 4 digit (AMEX)",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def cc_quantity_menu_callback(query, context):
    keyboard = [
        [InlineKeyboardButton("5", callback_data="cc_qty_5")],
        [InlineKeyboardButton("10", callback_data="cc_qty_10")],
        [InlineKeyboardButton("20", callback_data="cc_qty_20")],
        [InlineKeyboardButton("50", callback_data="cc_qty_50")],
        [InlineKeyboardButton("100", callback_data="cc_qty_100")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="cc_settings")]
    ]
    
    await query.edit_message_text(
        "📊 *Pilih Jumlah Kartu*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Pilih berapa banyak kartu yang akan digenerate:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def cc_generate_now_callback(query, context):
    user_data = context.user_data
    
    month = user_data.get('cc_month', 'random')
    year = user_data.get('cc_year', 'random')
    cvv = user_data.get('cc_cvv', 'random')
    quantity = user_data.get('cc_quantity', 10)
    bin_input = user_data.get('cc_bin', '')
    
    loading_msg = await query.edit_message_text("💳 Generating cards...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text(f"🔄 Generating {quantity} cards...")
    await asyncio.sleep(0.5)
    
    cards, valid_count = generate_cards(
        bin_input=bin_input,
        card_type='auto',
        quantity=quantity,
        month=month,
        year=year,
        cvv_mode=cvv,
        format_type='pipe'
    )
    
    if not cards:
        await loading_msg.edit_text("❌ Gagal generate kartu!")
        return
    
    result_text = f"💳 *GENERATED {len(cards)} CARDS*\n"
    result_text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    result_text += f"✅ Valid: {valid_count} | ❌ Invalid: {len(cards) - valid_count}\n\n"
    result_text += "📌 *Format: `number|MM|YY|CVV`*\n\n"
    
    for i, card in enumerate(cards[:15], 1):
        result_text += f"{i}. `{card['formatted']}`\n"
    
    if len(cards) > 15:
        result_text += f"\n_... dan {len(cards) - 15} kartu lainnya_"
    
    keyboard = [
        [InlineKeyboardButton("📁 Export Pipe", callback_data="export_pipe")],
        [InlineKeyboardButton("📁 Export Full", callback_data="export_full_cards")],
        [InlineKeyboardButton("⚙️ Pengaturan", callback_data="cc_settings")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
    ]
    
    await loading_msg.edit_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    user_data['last_cards'] = cards

# ============================================================
# TELEGRAM BOT HANDLERS
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🎯 *HIRAKOX TOOLKIT v3.0*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *FITUR TERSEDIA:*
• 🔍 BIN Lookup & Detail
• 🔢 Generate BIN + Validasi
• 💳 Generate Kartu Kredit
• 👤 Generate Identitas Palsu
• ✅ CC Checker (Live/Die)
• 📊 BIN Database (Scrape)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *Telegram:* @hirakox
📌 *Version:* 3.0

⚠️ *Untuk tujuan edukasi saja*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Pilih menu di bawah untuk memulai:
"""
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_data = context.user_data
    bindb = context.bot_data.get('bindb', BINDatabase())
    
    # ============ MAIN MENU ============
    if data == "bin":
        await query.edit_message_text(
            "🔍 *BIN LOOKUP & DETAIL*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *Cara Penggunaan:*\n"
            "• Kirim BIN: `/bin 414720`\n"
            "• Multiple: `/bin 414720 454789`\n"
            "• Upload file .txt berisi daftar BIN\n\n"
            "🔧 *Filter:*\n"
            "`/bin 414720 --vendor Visa --level Gold`\n\n"
            "📋 *Info yang didapat:*\n"
            "• Network, Card Type, Level\n"
            "• Bank Issuer\n"
            "• Country & Country Code\n\n"
            "📁 *Support:* Input manual & Upload file",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
        user_data['mode'] = 'bin'
    
    elif data == "genbin":
        await query.edit_message_text(
            "🔢 *GENERATE BIN + VALIDATE*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *Format:* `/genbin [suffix] [jumlah]`\n"
            "• Suffix: 1-9\n"
            "• Jumlah: default 10\n\n"
            "📝 *Contoh:*\n"
            "• `/genbin 5` (5 BIN suffix 5)\n"
            "• `/genbin 3 20` (20 BIN suffix 3)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
        user_data['mode'] = 'genbin'
    
    elif data == "generate":
        await query.edit_message_text(
            "💳 *CC GENERATOR*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *Cara Penggunaan:*\n"
            "• `/gen` - Generate dengan pengaturan\n"
            "• `/gen [BIN]` - Generate dengan BIN tertentu\n"
            "• `/gen [BIN] [jumlah]` - Dengan jumlah\n\n"
            "📝 *Contoh:*\n"
            "• `/gen 414720` (10 kartu)\n"
            "• `/gen 414720 20` (20 kartu)\n"
            "• `/gen random` (random BIN)\n\n"
            "⚙️ *Pengaturan:*\n"
            "Atur bulan, tahun, CVV sebelum generate",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ Pengaturan", callback_data="cc_settings")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
        user_data['mode'] = 'generate'
    
    elif data == "user":
        await query.edit_message_text(
            "👤 *FAKE USER GENERATOR*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *Cara Penggunaan:*\n"
            "• `/user` - 5 user random\n"
            "• `/user 10` - 10 user\n"
            "• `/user male 5` - 5 pria\n"
            "• `/user female 10` - 10 wanita\n"
            "• `/user US 10` - 10 dari US\n\n"
            "🌍 *Kode:* US, GB, CA, AU, DE, FR, IN",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
        user_data['mode'] = 'user'
    
    elif data == "checker":
        await query.edit_message_text(
            "✅ *CC CHECKER*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *Format:* `/check number|MM|YY|CVV`\n\n"
            "📝 *Contoh:*\n"
            "`/check 4147209876543210|12|26|123`\n\n"
            "📁 *Bulk Check:* Upload file .txt\n"
            "📊 *Hasil:* ✅ LIVE / ❌ DIE / ❓ UNKNOWN",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
        user_data['mode'] = 'checker'
    
    # ============ BIN DATABASE ============
    elif data == "bindb":
        # Tampilkan daftar negara yang tersedia
        countries = bindb.get_all_countries()
        user_data['bindb_countries'] = countries
        
        keyboard = []
        # Tampilkan 10 negara per halaman
        page = user_data.get('bindb_page', 0)
        per_page = 10
        start = page * per_page
        end = min(start + per_page, len(countries))
        
        for i, country in enumerate(countries[start:end], start+1):
            keyboard.append([InlineKeyboardButton(f"{i}. {country.title()}", callback_data=f"bindb_country_{country}")])
        
        # Navigasi
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data="bindb_prev"))
        if end < len(countries):
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data="bindb_next"))
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="back")])
        
        await query.edit_message_text(
            f"📊 *BIN DATABASE*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📌 *Pilih Negara* (halaman {page+1}/{(len(countries)-1)//per_page + 1}):\n"
            f"Total {len(countries)} negara tersedia.\n\n"
            f"Setelah memilih, masukkan jumlah BIN yang ingin diambil.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        user_data['mode'] = 'bindb'
    
    elif data == "bindb_prev":
        user_data['bindb_page'] = max(0, user_data.get('bindb_page', 0) - 1)
        await handle_callback_query(update, context)
    
    elif data == "bindb_next":
        user_data['bindb_page'] = user_data.get('bindb_page', 0) + 1
        await handle_callback_query(update, context)
    
    elif data.startswith("bindb_country_"):
        country = data.replace("bindb_country_", "")
        user_data['bindb_selected_country'] = country
        
        await query.edit_message_text(
            f"📊 *BIN DATABASE - {country.title()}*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📌 Masukkan jumlah BIN yang ingin diambil:\n"
            f"• Kirim angka (contoh: `50`)\n"
            f"• Kirim `all` untuk semua BIN\n\n"
            f"⏳ Proses scraping akan memakan waktu beberapa detik.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="bindb")]
            ]),
            parse_mode='Markdown'
        )
        user_data['mode'] = 'bindb_limit'
    
    elif data == "about":
        await query.edit_message_text(
            "ℹ️ *HIRAKOX TOOLKIT v3.0*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔥 *FITUR:*\n"
            "✓ BIN Lookup & Detail\n"
            "✓ Generate BIN dengan Suffix\n"
            "✓ Generate Kartu Kredit\n"
            "✓ Generate Identitas Palsu\n"
            "✓ CC Checker (Live/Die)\n"
            "✓ BIN Database (Scrape)\n\n"
            "⚡ *FITUR BOT:*\n"
            "✓ Format Pipe / Full\n"
            "✓ Output Text / File\n"
            "✓ Support Upload File\n"
            "✓ Bulk Processing\n\n"
            "💬 *Telegram:* @hirakox\n"
            "📌 *Version:* 3.0\n\n"
            "⚠️ *Untuk tujuan edukasi saja*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
    
    elif data == "help":
        await query.edit_message_text(
            "❓ *PANDUAN PENGGUNAAN*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔍 *BIN LOOKUP & DETAIL*\n"
            "`/bin 414720`\n"
            "`/bin 414720 454789`\n\n"
            "🔢 *GEN BIN + VALID*\n"
            "`/genbin 5`\n"
            "`/genbin 3 20`\n\n"
            "💳 *CC GENERATOR*\n"
            "`/gen` (dengan pengaturan)\n"
            "`/gen 414720` (dengan BIN)\n"
            "`/gen 414720 20` (dengan BIN & jumlah)\n\n"
            "👤 *FAKE USER*\n"
            "`/user`\n"
            "`/user male 5`\n\n"
            "✅ *CC CHECKER*\n"
            "`/check 414720...|12|26|123`\n\n"
            "📊 *BIN DATABASE*\n"
            "Pilih menu 'BIN Database' > Pilih negara > Masukkan jumlah\n\n"
            "📁 *Support File:* Upload .txt",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
    
    elif data == "back":
        welcome_text = """
🎯 *HIRAKOX TOOLKIT v3.0*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *FITUR TERSEDIA:*
• 🔍 BIN Lookup & Detail
• 🔢 Generate BIN + Validasi
• 💳 Generate Kartu Kredit
• 👤 Generate Identitas Palsu
• ✅ CC Checker (Live/Die)
• 📊 BIN Database (Scrape)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *Telegram:* @hirakox
📌 *Version:* 3.0

⚠️ *Untuk tujuan edukasi saja*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Pilih menu di bawah untuk memulai:
"""
        await query.edit_message_text(
            welcome_text,
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )
        user_data['mode'] = ''
    
    # ============ CC GENERATOR SETTINGS ============
    elif data == "cc_settings":
        await cc_generator_settings_callback(query, context)
    
    elif data == "cc_settings_back":
        await query.edit_message_text(
            "💳 *CC GENERATOR*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *Cara Penggunaan:*\n"
            "• `/gen` - Generate dengan pengaturan\n"
            "• `/gen [BIN]` - Generate dengan BIN tertentu\n"
            "• `/gen [BIN] [jumlah]` - Dengan jumlah\n\n"
            "📝 *Contoh:*\n"
            "• `/gen 414720` (10 kartu)\n"
            "• `/gen 414720 20` (20 kartu)\n"
            "• `/gen random` (random BIN)\n\n"
            "⚙️ *Pengaturan:*\n"
            "Atur bulan, tahun, CVV sebelum generate",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ Pengaturan", callback_data="cc_settings")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]),
            parse_mode='Markdown'
        )
    
    elif data == "cc_month":
        await cc_month_menu_callback(query, context)
    
    elif data == "cc_year":
        await cc_year_menu_callback(query, context)
    
    elif data == "cc_cvv":
        await cc_cvv_menu_callback(query, context)
    
    elif data == "cc_quantity":
        await cc_quantity_menu_callback(query, context)
    
    elif data.startswith("cc_month_"):
        month = data.replace("cc_month_", "")
        month_map = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        if month == 'random':
            user_data['cc_month'] = 'random'
        else:
            user_data['cc_month'] = month_map.get(month, 'random')
        await query.edit_message_text("✅ Bulan sudah diatur!")
        await asyncio.sleep(1)
        await cc_generator_settings_callback(query, context)
    
    elif data.startswith("cc_year_"):
        year = data.replace("cc_year_", "")
        if year == 'random':
            user_data['cc_year'] = 'random'
        else:
            user_data['cc_year'] = year
        await query.edit_message_text("✅ Tahun sudah diatur!")
        await asyncio.sleep(1)
        await cc_generator_settings_callback(query, context)
    
    elif data.startswith("cc_cvv_"):
        cvv = data.replace("cc_cvv_", "")
        user_data['cc_cvv'] = cvv
        cvv_names = {
            'random': 'Random (3 digit)',
            '3digit': '3 Digit',
            '4digit': '4 Digit'
        }
        await query.edit_message_text(f"✅ CVV sudah diatur: {cvv_names.get(cvv, cvv)}")
        await asyncio.sleep(1)
        await cc_generator_settings_callback(query, context)
    
    elif data.startswith("cc_qty_"):
        qty = data.replace("cc_qty_", "")
        user_data['cc_quantity'] = int(qty)
        await query.edit_message_text(f"✅ Jumlah sudah diatur: {qty}")
        await asyncio.sleep(1)
        await cc_generator_settings_callback(query, context)
    
    elif data == "cc_generate_now":
        await cc_generate_now_callback(query, context)
    
    # ============ BIN VALIDATION ============
    elif data == "validate_bin":
        if 'pending_bins' in user_data:
            bin_list = user_data['pending_bins']
            loading_msg = await query.edit_message_text("🔄 Validating BIN...")
            
            await asyncio.sleep(0.5)
            await loading_msg.edit_text("⏳ Mengirim request ke server...")
            await asyncio.sleep(0.5)
            await loading_msg.edit_text("🔍 Menganalisis data BIN...")
            await asyncio.sleep(0.5)
            
            html = search_bin(bin_list, {})
            if "Error" in html:
                await loading_msg.edit_text(f"❌ Error: {html}")
                return
            
            results = parse_bin_results(html)
            if results:
                result_text = f"✅ *Hasil Validasi {len(results)} BIN*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                for idx, item in enumerate(results[:20], 1):
                    result_text += f"*{idx}. BIN:* `{item['bin']}`\n"
                    result_text += f"   🌍 {item['country']} | 🏛️ {item['vendor']}\n"
                    result_text += f"   📋 {item['type']} | 📊 {item['level']}\n"
                    result_text += f"   🏦 {item['bank']}\n\n"
                
                if len(results) > 20:
                    result_text += f"_... dan {len(results) - 20} hasil lainnya_\n\n"
                
                keyboard = [
                    [InlineKeyboardButton("📁 Export ke File", callback_data="export_bin")],
                    [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
                ]
                await loading_msg.edit_text(
                    result_text,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
                user_data['bin_results'] = results
            else:
                await loading_msg.edit_text("❌ Tidak ada hasil ditemukan.")
    
    elif data == "skip_validate":
        await query.edit_message_text(
            "⏭️ Validasi dilewati.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ])
        )
    
    # ============ EXPORTS ============
    elif data == "export_bin":
        if 'bin_results' in user_data:
            results = user_data['bin_results']
            await query.edit_message_text("📁 Generating file...")
            
            output = "BIN|Country|Vendor|Type|Level|Bank\n"
            for item in results:
                output += f"{item['bin']}|{item['country']}|{item['vendor']}|{item['type']}|{item['level']}|{item['bank']}\n"
            
            file = BytesIO(output.encode('utf-8'))
            file.name = f"bin_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            await query.message.reply_document(
                document=file,
                caption=f"🔍 {len(results)} BIN results"
            )
            await query.edit_message_text("✅ File berhasil di export!")
    
    elif data == "export_scrape":
        if 'scraped_bins' in user_data:
            bins = user_data['scraped_bins']
            await query.edit_message_text("📁 Generating file...")
            
            output = "BIN|Network|Card Type|Level|Country\n"
            for b in bins:
                output += f"{b['BIN']}|{b['Network']}|{b['Card Type']}|{b['Level']}|{b['Country']}\n"
            
            file = BytesIO(output.encode('utf-8'))
            file.name = f"bindb_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            await query.message.reply_document(
                document=file,
                caption=f"📊 {len(bins)} BIN dari database"
            )
            await query.edit_message_text("✅ File berhasil di export!")
    
    elif data == "export_live":
        if 'checker_results' in user_data:
            results = user_data['checker_results']
            await query.edit_message_text("📁 Generating LIVE cards...")
            
            output = "Card Number|MM|YY|CVV\n"
            count = 0
            for r in results:
                if r.get('error', 3) == 1:
                    card_data = r.get('card', r.get('input', ''))
                    parts = card_data.split('|')
                    if len(parts) >= 4:
                        year = parts[2]
                        if len(year) == 4:
                            year = year[2:]
                        output += f"{parts[0]}|{parts[1].zfill(2)}|{year}|{parts[3]}\n"
                        count += 1
            
            if count > 0:
                file = BytesIO(output.encode('utf-8'))
                file.name = f"live_cards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                await query.message.reply_document(
                    document=file,
                    caption=f"✅ {count} LIVE cards"
                )
                await query.edit_message_text(f"✅ {count} LIVE cards berhasil di export!")
            else:
                await query.edit_message_text("❌ Tidak ada LIVE cards!")
    
    elif data == "export_full":
        if 'checker_results' in user_data:
            results = user_data['checker_results']
            await query.edit_message_text("📁 Generating full report...")
            
            output = f"CC Checker Results - {datetime.now()}\n"
            output += "=" * 60 + "\n\n"
            for r in results:
                if "error" in r and isinstance(r.get('error'), str):
                    output += f"[ERROR] {r.get('input', '-')} - {r['error']}\n"
                else:
                    code = r.get('error', 3)
                    status = "LIVE" if code == 1 else "DIE" if code == 2 else "UNKNOWN"
                    output += f"[{status}] {r.get('input', '-')}\n"
                    if 'network' in r and r['network']:
                        output += f"  Network : {r['network']}\n"
                    if 'message' in r and r['message']:
                        output += f"  Message : {r['message']}\n"
                    if 'score' in r and r['score']:
                        output += f"  Score   : {r['score']}%\n"
                    if 'card' in r and r['card']:
                        output += f"  Card    : {r['card']}\n"
                    output += "-" * 40 + "\n"
            
            file = BytesIO(output.encode('utf-8'))
            file.name = f"full_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            await query.message.reply_document(
                document=file,
                caption=f"📊 Full Report - {len(results)} cards"
            )
            await query.edit_message_text("✅ Full report berhasil di export!")
    
    elif data == "export_pipe":
        if 'last_cards' in user_data:
            cards = user_data['last_cards']
            await query.edit_message_text("📁 Generating pipe format...")
            
            output = "Number|MM|YY|CVV\n"
            for card in cards:
                output += f"{card['number']}|{card['month']}|{card['year']}|{card['cvv']}\n"
            
            file = BytesIO(output.encode('utf-8'))
            file.name = f"cards_pipe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            await query.message.reply_document(
                document=file,
                caption=f"💳 {len(cards)} cards (Pipe format)"
            )
            await query.edit_message_text("✅ File berhasil di export!")
    
    elif data == "export_full_cards":
        if 'last_cards' in user_data:
            cards = user_data['last_cards']
            await query.edit_message_text("📁 Generating full format...")
            
            output = "Card Number|Type|Month|Year|CVV|Status\n"
            for card in cards:
                status = "VALID" if card['is_valid'] else "INVALID"
                output += f"{card['number']}|{card['type_name']}|{card['month']}|{card['year']}|{card['cvv']}|{status}\n"
            
            file = BytesIO(output.encode('utf-8'))
            file.name = f"cards_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            await query.message.reply_document(
                document=file,
                caption=f"💳 {len(cards)} cards (Full format)"
            )
            await query.edit_message_text("✅ File berhasil di export!")
    
    elif data == "export_users":
        if 'last_users' in user_data:
            users = user_data['last_users']
            await query.edit_message_text("📁 Generating users file...")
            
            output = "Name|Email|Phone|DOB|Gender|Country|Address\n"
            for user in users:
                output += f"{user['name']}|{user['email']}|{user['phone']}|{user['dob']}|{user['gender']}|{user['country']}|{user['address']}\n"
            
            file = BytesIO(output.encode('utf-8'))
            file.name = f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            await query.message.reply_document(
                document=file,
                caption=f"👤 {len(users)} users"
            )
            await query.edit_message_text("✅ File berhasil di export!")

# ============================================================
# HANDLE MESSAGE
# ============================================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        await handle_file(update, context)
        return
    
    text = update.message.text
    if not text:
        return
    
    if text.startswith('/'):
        await handle_command(update, context)
        return
    
    mode = context.user_data.get('mode', '')
    
    if mode == 'bin':
        await handle_bin_lookup(update, context)
    elif mode == 'genbin':
        await handle_genbin(update, context)
    elif mode == 'generate':
        await handle_generate_cards(update, context)
    elif mode == 'user':
        await handle_user_generate(update, context)
    elif mode == 'checker':
        await handle_cc_checker(update, context)
    elif mode == 'bindb_limit':
        await handle_bindb_limit(update, context)
    else:
        welcome_text = """
🎯 *HIRAKOX TOOLKIT v3.0*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *FITUR TERSEDIA:*
• 🔍 BIN Lookup & Detail
• 🔢 Generate BIN + Validasi
• 💳 Generate Kartu Kredit
• 👤 Generate Identitas Palsu
• ✅ CC Checker (Live/Die)
• 📊 BIN Database (Scrape)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *Telegram:* @hirakox
📌 *Version:* 3.0

⚠️ *Untuk tujuan edukasi saja*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Pilih menu di bawah untuk memulai:
"""
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )

# ============================================================
# HANDLE FILE
# ============================================================
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_name = document.file_name
    
    if not file_name.endswith('.txt'):
        await update.message.reply_text("❌ Hanya file .txt yang didukung!")
        return
    
    file = await document.get_file()
    file_content = await file.download_as_bytearray()
    content = file_content.decode('utf-8')
    
    mode = context.user_data.get('mode', '')
    
    if mode == 'bin':
        loading_msg = await update.message.reply_text("📁 Memproses file...")
        await asyncio.sleep(0.5)
        await loading_msg.edit_text("🔍 Membaca data BIN dari file...")
        await asyncio.sleep(0.5)
        
        bin_list = []
        for line in content.split('\n'):
            for part in re.sub(r'[,;\s]+', ' ', line.strip()).split():
                if part.isdigit() and len(part) >= 6:
                    bin_list.append(part)
        
        if not bin_list:
            await loading_msg.edit_text("❌ Tidak ada BIN valid di file!")
            return
        
        if len(bin_list) > 100:
            await loading_msg.edit_text("⚠️ Maksimal 100 BIN per file!")
            bin_list = bin_list[:100]
        
        await loading_msg.edit_text(f"📁 Memproses {len(bin_list)} BIN...")
        
        html = search_bin(bin_list, {})
        if "Error" in html:
            await loading_msg.edit_text(f"❌ Error: {html}")
            return
        
        results = parse_bin_results(html)
        if results:
            result_text = f"✅ *Hasil {len(results)} BIN*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            for idx, item in enumerate(results[:20], 1):
                result_text += f"*{idx}. BIN:* `{item['bin']}`\n"
                result_text += f"   🌍 {item['country']} | 🏛️ {item['vendor']}\n"
                result_text += f"   📋 {item['type']} | 📊 {item['level']}\n"
                result_text += f"   🏦 {item['bank']}\n\n"
            
            if len(results) > 20:
                result_text += f"_... dan {len(results) - 20} hasil lainnya_"
            
            keyboard = [
                [InlineKeyboardButton("📁 Export ke File", callback_data="export_bin")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
            ]
            await loading_msg.edit_text(
                result_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            context.user_data['bin_results'] = results
        else:
            await loading_msg.edit_text("❌ Tidak ada hasil ditemukan.")
    
    elif mode == 'checker':
        loading_msg = await update.message.reply_text("📁 Memproses file...")
        await asyncio.sleep(0.5)
        await loading_msg.edit_text("🔍 Membaca data kartu dari file...")
        await asyncio.sleep(0.5)
        
        cards = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                cards.append(line)
        
        if not cards:
            await loading_msg.edit_text("❌ Tidak ada data kartu di file!")
            return
        
        if len(cards) > 20:
            await loading_msg.edit_text("⚠️ Maksimal 20 kartu per file!")
            cards = cards[:20]
        
        await loading_msg.edit_text(f"📁 Memproses {len(cards)} kartu...")
        
        results = []
        live = die = unknown = 0
        result_text = "✅ *CC CHECKER RESULTS*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, raw in enumerate(cards, 1):
            await loading_msg.edit_text(f"⏳ Memeriksa kartu {i}/{len(cards)}...")
            
            formatted = parse_card_netverse(raw)
            if not formatted:
                result_text += f"{i}. ❌ Invalid format\n"
                continue
            
            if i > 1:
                time.sleep(1.5)
            
            result = check_card_netverse(formatted)
            result['input'] = raw
            results.append(result)
            
            code = result.get('error', 3)
            if code == 1:
                live += 1
                status_icon = "✅ LIVE"
            elif code == 2:
                die += 1
                status_icon = "❌ DIE"
            else:
                unknown += 1
                status_icon = "❓ UNKNOWN"
            
            card_display = raw[:24] + "..." if len(raw) > 24 else raw
            result_text += f"{i}. {status_icon} | `{card_display}`\n"
            if 'network' in result and result['network']:
                result_text += f"   🏷️ {result['network']}\n"
            result_text += "\n"
        
        result_text += f"📊 *SUMMARY*\n"
        result_text += f"• Total: {len(cards)}\n"
        result_text += f"• ✅ Live: {live}\n"
        result_text += f"• ❌ Die: {die}\n"
        result_text += f"• ❓ Unknown: {unknown}\n"
        
        keyboard = [
            [InlineKeyboardButton("📁 Export LIVE Cards", callback_data="export_live")],
            [InlineKeyboardButton("📁 Export Full Report", callback_data="export_full")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
        ]
        await loading_msg.edit_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        context.user_data['checker_results'] = results
    
    else:
        welcome_text = """
🎯 *HIRAKOX TOOLKIT v3.0*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *FITUR TERSEDIA:*
• 🔍 BIN Lookup & Detail
• 🔢 Generate BIN + Validasi
• 💳 Generate Kartu Kredit
• 👤 Generate Identitas Palsu
• ✅ CC Checker (Live/Die)
• 📊 BIN Database (Scrape)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *Telegram:* @hirakox
📌 *Version:* 3.0

⚠️ *Untuk tujuan edukasi saja*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Pilih menu di bawah untuk memulai:
"""
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )

# ============================================================
# BIN DATABASE LIMIT HANDLER
# ============================================================
async def handle_bindb_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk input jumlah BIN dari BIN Database"""
    text = update.message.text.strip()
    user_data = context.user_data
    bindb = context.bot_data.get('bindb', BINDatabase())
    
    country = user_data.get('bindb_selected_country')
    if not country:
        await update.message.reply_text("❌ Silakan pilih negara terlebih dahulu dari menu BIN Database!")
        return
    
    # Parse limit
    if text.lower() == 'all':
        limit = None
    elif text.isdigit():
        limit = int(text)
        if limit < 1:
            await update.message.reply_text("❌ Jumlah harus lebih dari 0!")
            return
    else:
        await update.message.reply_text("❌ Masukkan angka yang valid atau 'all'!")
        return
    
    loading_msg = await update.message.reply_text(f"📊 Mengambil BIN dari {country.title()}...\n⏳ Mohon tunggu...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text(f"🔄 Scraping {country.title()}...")
    await asyncio.sleep(0.5)
    
    # Scrape BIN
    bins = bindb.scrape_bins(country, limit)
    
    if not bins:
        await loading_msg.edit_text(f"❌ Tidak ada BIN ditemukan untuk {country.title()}!")
        return
    
    user_data['scraped_bins'] = bins
    
    # Tampilkan hasil
    country_count = {}
    for b in bins:
        country_count[b['Country']] = country_count.get(b['Country'], 0) + 1
    
    result_text = f"📊 *BIN DATABASE - {country.title()}*\n"
    result_text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    result_text += f"Total BIN: {len(bins)}\n\n"
    
    if len(bins) > 0:
        result_text += "📋 *Sample 10 BIN pertama:*\n"
        result_text += "```\n"
        result_text += f"{'BIN':<12} | {'Network':<12} | {'Level':<12}\n"
        result_text += "-"*40 + "\n"
        for b in bins[:10]:
            result_text += f"{b['BIN']:<12} | {b['Network']:<12} | {b['Level']:<12}\n"
        result_text += "```"
    
    if len(bins) > 10:
        result_text += f"\n_... dan {len(bins)-10} BIN lainnya_"
    
    keyboard = [
        [InlineKeyboardButton("📁 Export ke File", callback_data="export_scrape")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="bindb")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="back")]
    ]
    
    await loading_msg.edit_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# ============================================================
# HANDLE COMMANDS
# ============================================================
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split()
    command = parts[0].lower()
    bindb = context.bot_data.get('bindb', BINDatabase())
    
    if command == '/bin':
        await handle_bin_lookup(update, context)
    elif command == '/genbin':
        await handle_genbin(update, context)
    elif command == '/gen':
        if len(parts) > 1:
            context.user_data['cc_bin'] = parts[1]
            if len(parts) > 2 and parts[2].isdigit():
                context.user_data['cc_quantity'] = int(parts[2])
        else:
            context.user_data['cc_bin'] = ''
        
        if 'cc_month' not in context.user_data:
            context.user_data['cc_month'] = 'random'
        if 'cc_year' not in context.user_data:
            context.user_data['cc_year'] = 'random'
        if 'cc_cvv' not in context.user_data:
            context.user_data['cc_cvv'] = 'random'
        if 'cc_quantity' not in context.user_data:
            context.user_data['cc_quantity'] = 10
        
        await handle_generate_cards(update, context)
    
    elif command == '/genfull':
        context.user_data['card_format'] = 'full'
        await handle_generate_cards(update, context)
    elif command == '/genpipe':
        context.user_data['card_format'] = 'pipe'
        await handle_generate_cards(update, context)
    elif command == '/user':
        await handle_user_generate(update, context)
    elif command == '/check':
        await handle_cc_checker(update, context)
    elif command == '/bindb':
        # Tampilkan daftar negara
        countries = bindb.get_all_countries()
        context.user_data['bindb_countries'] = countries
        
        keyboard = []
        for i, country in enumerate(countries[:10], 1):
            keyboard.append([InlineKeyboardButton(f"{i}. {country.title()}", callback_data=f"bindb_country_{country}")])
        keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="back")])
        
        await update.message.reply_text(
            "📊 *BIN DATABASE*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📌 *Pilih Negara:*\n"
            f"Total {len(countries)} negara tersedia.\n\n"
            f"Setelah memilih, masukkan jumlah BIN yang ingin diambil.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        context.user_data['mode'] = 'bindb'
    else:
        welcome_text = """
🎯 *HIRAKOX TOOLKIT v3.0*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *FITUR TERSEDIA:*
• 🔍 BIN Lookup & Detail
• 🔢 Generate BIN + Validasi
• 💳 Generate Kartu Kredit
• 👤 Generate Identitas Palsu
• ✅ CC Checker (Live/Die)
• 📊 BIN Database (Scrape)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *Telegram:* @hirakox
📌 *Version:* 3.0

⚠️ *Untuk tujuan edukasi saja*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Pilih menu di bawah untuk memulai:
"""
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )

# ============================================================
# BIN LOOKUP (DENGAN DETAIL)
# ============================================================
async def handle_bin_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split()
    bindb = context.bot_data.get('bindb', BINDatabase())
    
    if parts and parts[0] in ['/bin']:
        parts = parts[1:]
    
    if not parts:
        await update.message.reply_text(
            "🔍 *BIN LOOKUP & DETAIL*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 Kirim BIN (6-8 digit):\n"
            "Contoh: `414720` atau `414720 454789`\n\n"
            "📋 *Info yang didapat:*\n"
            "• Network (Visa/Mastercard/AMEX)\n"
            "• Card Type (Credit/Debit)\n"
            "• Level (Platinum/Standard/Gold)\n"
            "• Bank Issuer\n"
            "• Country & Country Code\n\n"
            "📁 Atau upload file .txt",
            parse_mode='Markdown'
        )
        return
    
    # Cek apakah single BIN atau multiple
    bin_list = []
    filters = {}
    i = 0
    
    while i < len(parts):
        if parts[i].startswith('--'):
            if i + 1 < len(parts):
                filters[parts[i][2:]] = parts[i+1]
                i += 2
            else:
                i += 1
        else:
            if parts[i].isdigit() and len(parts[i]) >= 6:
                bin_list.append(parts[i])
            i += 1
    
    if not bin_list:
        await update.message.reply_text("❌ Tidak ada BIN valid!")
        return
    
    # Jika hanya 1 BIN, tampilkan detail lengkap
    if len(bin_list) == 1:
        bin_num = bin_list[0]
        loading_msg = await update.message.reply_text(f"🔄 Mencari detail BIN {bin_num}...")
        await asyncio.sleep(0.5)
        await loading_msg.edit_text("⏳ Mengakses server...")
        await asyncio.sleep(0.5)
        await loading_msg.edit_text(f"🔍 Mengambil detail BIN {bin_num}...")
        await asyncio.sleep(0.5)
        
        detail = bindb.get_bin_detail(bin_num)
        
        if detail:
            result_text = f"🔍 *DETAIL BIN: {detail['BIN']}*\n"
            result_text += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            result_text += f"📌 *Card Information:*\n"
            result_text += f"  • Network      : `{detail['Network']}`\n"
            result_text += f"  • Card Type    : `{detail['Card Type']}`\n"
            result_text += f"  • Level        : `{detail['Level']}`\n\n"
            result_text += f"🏦 *Bank Issuer:*\n"
            result_text += f"  • Bank Name    : `{detail['Bank']}`\n\n"
            result_text += f"🌏 *Country Issuer:*\n"
            result_text += f"  • Country      : `{detail['Country']}`\n"
            result_text += f"  • Country Code : `{detail['Country Code']}`\n"
            
            keyboard = [
                [InlineKeyboardButton("🔙 Kembali", callback_data="back")],
                [InlineKeyboardButton("🔍 Cek BIN Lain", callback_data="bin")]
            ]
            await loading_msg.edit_text(
                result_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        else:
            await loading_msg.edit_text(f"❌ Gagal mendapatkan detail BIN {bin_num}. Coba lagi nanti.")
        return
    
    # Multiple BIN - gunakan search biasa
    if len(bin_list) > 50:
        await update.message.reply_text("⚠️ Maksimal 50 BIN per request!")
        bin_list = bin_list[:50]
    
    loading_msg = await update.message.reply_text("🔄 Mencari BIN...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text("⏳ Mengirim request ke server...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text(f"🔍 Mencari {len(bin_list)} BIN...")
    await asyncio.sleep(0.5)
    
    html = search_bin(bin_list, filters)
    if "Error" in html:
        await loading_msg.edit_text(f"❌ Error: {html}")
        return
    
    results = parse_bin_results(html)
    
    if results:
        result_text = f"✅ *Hasil {len(results)} BIN*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for idx, item in enumerate(results[:20], 1):
            result_text += f"*{idx}. BIN:* `{item['bin']}`\n"
            result_text += f"   🌍 {item['country']} | 🏛️ {item['vendor']}\n"
            result_text += f"   📋 {item['type']} | 📊 {item['level']}\n"
            result_text += f"   🏦 {item['bank']}\n\n"
        
        if len(results) > 20:
            result_text += f"_... dan {len(results) - 20} hasil lainnya_"
        
        keyboard = [
            [InlineKeyboardButton("📁 Export ke File", callback_data="export_bin")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
        ]
        await loading_msg.edit_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        context.user_data['bin_results'] = results
    else:
        await loading_msg.edit_text("❌ Tidak ada hasil ditemukan.")

# ============================================================
# GEN BIN + VALID
# ============================================================
async def handle_genbin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split()
    
    if parts and parts[0] in ['/genbin']:
        parts = parts[1:]
    
    if not parts:
        await update.message.reply_text(
            "🔢 *GEN BIN + VALIDATE*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 Format: `/genbin [suffix] [jumlah]`\n"
            "• Suffix: 1-9\n"
            "• Jumlah: default 10\n\n"
            "📝 Contoh:\n"
            "• `/genbin 5`\n"
            "• `/genbin 3 20`",
            parse_mode='Markdown'
        )
        return
    
    suffix = parts[0]
    if not suffix.isdigit() or int(suffix) < 1 or int(suffix) > 9:
        await update.message.reply_text("❌ Suffix harus angka 1-9!")
        return
    
    count = 10
    if len(parts) > 1 and parts[1].isdigit():
        count = min(int(parts[1]), 50)
    
    loading_msg = await update.message.reply_text(f"🔄 Generating {count} BIN...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text(f"🔢 Generating BIN dengan suffix {suffix}...")
    await asyncio.sleep(0.5)
    
    bin_list = generate_bins_with_suffix(suffix, count)
    
    result_text = f"🔢 *Generated {count} BIN*\n━━━━━━━━━━━━━━━━━━━━\n\n"
    for idx, bin_num in enumerate(bin_list, 1):
        result_text += f"{idx}. `{bin_num}`\n"
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Validasi", callback_data="validate_bin"),
            InlineKeyboardButton("❌ Skip", callback_data="skip_validate")
        ]
    ]
    
    await loading_msg.edit_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    
    context.user_data['pending_bins'] = bin_list

# ============================================================
# CC GENERATOR
# ============================================================
async def handle_generate_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split()
    
    month = context.user_data.get('cc_month', 'random')
    year = context.user_data.get('cc_year', 'random')
    cvv_mode = context.user_data.get('cc_cvv', 'random')
    quantity = context.user_data.get('cc_quantity', 10)
    bin_input = context.user_data.get('cc_bin', '')
    
    if parts and parts[0] in ['/gen', '/genfull', '/genpipe']:
        parts = parts[1:]
    
    if parts:
        if parts[0] != 'random':
            bin_input = parts[0]
        if len(parts) > 1 and parts[1].isdigit():
            quantity = min(int(parts[1]), 50)
        if len(parts) > 2 and parts[2].isdigit():
            year = parts[2]
    
    if bin_input.lower() == 'random':
        bin_input = ''
    
    format_type = context.user_data.get('card_format', 'pipe')
    
    loading_msg = await update.message.reply_text("💳 Generating cards...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text(f"🔄 Generating {quantity} cards...")
    await asyncio.sleep(0.5)
    
    cards, valid_count = generate_cards(
        bin_input=bin_input,
        card_type='auto',
        quantity=quantity,
        month=month,
        year=year,
        cvv_mode=cvv_mode,
        format_type=format_type
    )
    
    if not cards:
        await loading_msg.edit_text("❌ Gagal generate kartu!")
        return
    
    if format_type == 'pipe':
        result_text = f"💳 *GENERATED {len(cards)} CARDS*\n"
        result_text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        result_text += f"✅ Valid: {valid_count} | ❌ Invalid: {len(cards) - valid_count}\n\n"
        result_text += "📌 *Format: `number|MM|YY|CVV`*\n\n"
        
        for i, card in enumerate(cards[:15], 1):
            result_text += f"{i}. `{card['formatted']}`\n"
        
        if len(cards) > 15:
            result_text += f"\n_... dan {len(cards) - 15} kartu lainnya_"
        
    else:
        result_text = f"💳 *GENERATED {len(cards)} CARDS*\n"
        result_text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        result_text += f"✅ Valid: {valid_count} | ❌ Invalid: {len(cards) - valid_count}\n\n"
        
        for i, card in enumerate(cards[:10], 1):
            formatted = ' '.join(card['number'][j:j+4] for j in range(0, len(card['number']), 4))
            status_icon = "✅" if card['is_valid'] else "❌"
            result_text += f"*{i}. `{formatted}`* {status_icon}\n"
            result_text += f"   🏷️ {card['type_name']} | {card['month']}/{card['year']} | CVV: `{card['cvv']}`\n\n"
        
        if len(cards) > 10:
            result_text += f"_... dan {len(cards) - 10} kartu lainnya_"
    
    keyboard = [
        [InlineKeyboardButton("📁 Export Pipe", callback_data="export_pipe")],
        [InlineKeyboardButton("📁 Export Full", callback_data="export_full_cards")],
        [InlineKeyboardButton("⚙️ Pengaturan", callback_data="cc_settings")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
    ]
    
    await loading_msg.edit_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    context.user_data['last_cards'] = cards

# ============================================================
# USER GENERATOR
# ============================================================
async def handle_user_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split()
    
    if parts and parts[0] in ['/user']:
        parts = parts[1:]
    
    quantity = 5
    gender = 'random'
    nationality = 'US'
    
    for part in parts:
        if part.isdigit():
            quantity = min(int(part), 20)
        elif part.lower() in ['male', 'female']:
            gender = part.lower()
        elif part.upper() in ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'IN']:
            nationality = part.upper()
    
    loading_msg = await update.message.reply_text("👤 Generating users...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text(f"🔄 Generating {quantity} users...")
    await asyncio.sleep(0.5)
    
    users = generate_users(quantity, gender, nationality)
    
    if not users:
        await loading_msg.edit_text("❌ Gagal generate user!")
        return
    
    result_text = f"👤 *GENERATED {len(users)} USERS*\n"
    result_text += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, user in enumerate(users, 1):
        result_text += f"*{i}. {user['name']}*\n"
        result_text += f"   📧 {user['email']}\n"
        result_text += f"   📱 {user['phone']}\n"
        result_text += f"   🎂 {user['dob']}\n"
        result_text += f"   🏳️ {user['gender']} | 🌍 {user['country']}\n"
        result_text += f"   📍 {user['address']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("📁 Export ke File", callback_data="export_users")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
    ]
    await loading_msg.edit_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    context.user_data['last_users'] = users

# ============================================================
# CC CHECKER
# ============================================================
async def handle_cc_checker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lines = text.strip().split('\n')
    
    if lines and lines[0].startswith('/check'):
        lines = [line.replace('/check', '').strip() for line in lines if line.strip()]
    else:
        lines = [line.strip() for line in lines if line.strip() and not line.startswith('/')]
    
    if not lines:
        await update.message.reply_text(
            "✅ *CC CHECKER*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 Format: `number|MM|YY|CVV`\n"
            "Contoh: `/check 4147209876543210|12|26|123`\n\n"
            "📁 Upload file .txt untuk bulk check",
            parse_mode='Markdown'
        )
        return
    
    if len(lines) > 10:
        await update.message.reply_text("⚠️ Maksimal 10 kartu per request!")
        lines = lines[:10]
    
    loading_msg = await update.message.reply_text("✅ Checking cards...")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text(f"🔄 Checking {len(lines)} cards...")
    await asyncio.sleep(0.5)
    
    results = []
    live = die = unknown = 0
    result_text = "✅ *CC CHECKER RESULTS*\n"
    result_text += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, raw in enumerate(lines, 1):
        await loading_msg.edit_text(f"⏳ Memeriksa kartu {i}/{len(lines)}...")
        
        formatted = parse_card_netverse(raw)
        if not formatted:
            result_text += f"{i}. ❌ Invalid format\n"
            continue
        
        if i > 1:
            time.sleep(1.5)
        
        result = check_card_netverse(formatted)
        result['input'] = raw
        results.append(result)
        
        code = result.get('error', 3)
        if code == 1:
            live += 1
            status_icon = "✅ LIVE"
        elif code == 2:
            die += 1
            status_icon = "❌ DIE"
        else:
            unknown += 1
            status_icon = "❓ UNKNOWN"
        
        card_display = raw[:24] + "..." if len(raw) > 24 else raw
        result_text += f"{i}. {status_icon} | `{card_display}`\n"
        if 'network' in result and result['network']:
            result_text += f"   🏷️ Network: {result['network']}\n"
        if 'message' in result and result['message']:
            result_text += f"   📝 {result['message']}\n"
        result_text += "\n"
    
    result_text += f"📊 *SUMMARY*\n"
    result_text += f"• Total: {len(lines)}\n"
    result_text += f"• ✅ Live: {live}\n"
    result_text += f"• ❌ Die: {die}\n"
    result_text += f"• ❓ Unknown: {unknown}\n"
    
    keyboard = [
        [InlineKeyboardButton("📁 Export LIVE Cards", callback_data="export_live")],
        [InlineKeyboardButton("📁 Export Full Report", callback_data="export_full")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
    ]
    await loading_msg.edit_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    context.user_data['checker_results'] = results

# ============================================================
# MAIN
# ============================================================
def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "=" * 50)
        print("  ⚠️  TOKEN BELUM DIATUR  ⚠️")
        print("=" * 50)
        print("\n  Silakan ganti BOT_TOKEN di script")
        print("  dengan token dari @BotFather")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("  🚀 STARTING TELEGRAM BOT...")
    print("=" * 50)
    print("  💬 Bot: HIRAKOX TOOLKIT")
    print("  📡 Status: ONLINE")
    print("=" * 50)
    print("  Press Ctrl+C to stop\n")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Simpan bindb instance ke bot_data
    application.bot_data['bindb'] = BINDatabase()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("bin", handle_bin_lookup))
    application.add_handler(CommandHandler("genbin", handle_genbin))
    application.add_handler(CommandHandler("gen", handle_generate_cards))
    application.add_handler(CommandHandler("genfull", handle_generate_cards))
    application.add_handler(CommandHandler("genpipe", handle_generate_cards))
    application.add_handler(CommandHandler("user", handle_user_generate))
    application.add_handler(CommandHandler("check", handle_cc_checker))
    application.add_handler(CommandHandler("bindb", handle_command))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [+] Bot stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  [!] Error: {e}")
        sys.exit(1)
