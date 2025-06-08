import requests
import re

def find_working_selcuksportshd(start=1825, end=1850):
    print("🧭 Selcuksportshd domainleri taranıyor...")
    headers = {"User-Agent": "Mozilla/5.0"}

    for i in range(start, end + 1):
        url = f"https://www.selcuksportshd{i}.xyz/"
        print(f"🔍 Taranıyor: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200 and "uxsyplayer" in response.text:
                print(f"✅ Aktif domain bulundu: {url}")
                return response.text, url
        except:
            print(f"⚠️ Hata: {url}")
            continue

    print("❌ Aktif domain bulunamadı.")
    return None, None

def find_dynamic_player_domain(page_html):
    match = re.search(r'https?://(main\.uxsyplayer[0-9a-zA-Z\-]+\.click)', page_html)
    if match:
        return f"https://{match.group(1)}"
    return None

def extract_base_stream_url(html):
    match = re.search(r'this\.baseStreamUrl\s*=\s*[\'"]([^\'"]+)', html)
    if match:
        return match.group(1)
    return None

def build_m3u8_links(base_stream_url, channel_ids):
    m3u8_links = []
    for cid in channel_ids:
        full_url = f"{base_stream_url}{cid}/playlist.m3u8"
        print(f"✅ M3U8 link oluşturuldu: {full_url}")
        m3u8_links.append((cid, full_url))
    return m3u8_links

def update_m3u_file_with_referer_and_links(m3u8_list, filename="5.m3u", referer=referer_url)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["#EXTM3U\n"]

    updated_lines = []
    i = 0
    total_channels = len(m3u8_links)

    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF:-1"):
            updated_lines.append(line)
            i += 1
            # Eski URL ve Referer satırlarını atla
            while i < len(lines) and (lines[i].startswith("http") or lines[i].startswith("# Referer:")):
                i += 1

            kanal_adi = line.strip().split(',', 1)[1].strip()
            url_to_write = None
            for cid, url in m3u8_links:
                if cid.lower() in kanal_adi.lower():
                    url_to_write = url
                    break

            if url_to_write:
                updated_lines.append(f"# Referer: {referer}\n")
                updated_lines.append(f"{url_to_write}\n")
            else:
                updated_lines.append("\n")
        else:
            updated_lines.append(line)
            i += 1

    # Yeni kanalları ekle
    existing_channels = [l for l in updated_lines if l.startswith("#EXTINF:-1")]
    for cid, url in m3u8_links:
        if not any(cid.lower() in l.lower() for l in existing_channels):
            updated_lines.append(f"#EXTINF:-1,{cid}\n")
            updated_lines.append(f"# Referer: {referer}\n")
            updated_lines.append(f"{url}\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"\n💾 M3U dosyası güncellendi: {filename}")


# Kanal ID'leri
channel_ids = [
    "selcukbeinsports1",
    "selcukbeinsports2",
    "selcukbeinsports3",
    "selcukbeinsports4",
    "selcukbeinsports5"
]

# Ana işlem
html, referer_url = find_working_selcuksportshd()

if html:
    stream_domain = find_dynamic_player_domain(html)
    if stream_domain:
        print(f"\n🔗 Yayın domaini bulundu: {stream_domain}")
        try:
            player_page = requests.get(f"{stream_domain}/index.php?id={channel_ids[0]}",
                                       headers={"User-Agent": "Mozilla/5.0", "Referer": referer_url})
            base_stream_url = extract_base_stream_url(player_page.text)
            if base_stream_url:
                print(f"📡 Base stream URL bulundu: {base_stream_url}")
                m3u8_list = build_m3u8_links(base_stream_url, channel_ids)
                write_m3u_file(m3u8_list, referer=referer_url)
            else:
                print("❌ baseStreamUrl bulunamadı.")
        except Exception as e:
            print(f"⚠️ Hata oluştu: {e}")
    else:
        print("❌ Yayın domaini bulunamadı.")
else:
    print("⛔ Aktif yayın alınamadı.")
