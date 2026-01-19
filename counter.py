#!/usr/bin/env python3
"""
Hızlı Log Parser - IP Frekans Analizi
"""

import sys
from pathlib import Path


def parse_log_file(filepath):
    """Log dosyasını okuyup IP istatistiklerini hesaplar."""
    ip_stats = {}
    processed_lines = 0
    
    try:
        log_file = Path(filepath)
        
        if not log_file.exists():
            print(f"Hata: '{filepath}' bulunamadı!")
            return None
            
        with log_file.open('r', encoding='utf-8') as f:
            for line in f:
                processed_lines += 1
                
                # IP adresini satırdan çıkar
                if 'Connection from' in line:
                    # Son kelimeyi al (IP adresi)
                    words = line.split()
                    if words:
                        ip = words[-1]
                        # Basit IP kontrolü
                        if '.' in ip and len(ip.split('.')) == 4:
                            ip_stats[ip] = ip_stats.get(ip, 0) + 1
        
        return {
            'stats': ip_stats,
            'total_lines': processed_lines,
            'unique_ips': len(ip_stats)
        }
        
    except Exception as e:
        print(f"İşlem sırasında hata: {e}")
        return None


def display_results(analysis_data):
    """Analiz sonuçlarını ekranda gösterir."""
    if not analysis_data:
        return
    
    stats = analysis_data['stats']
    
    if not stats:
        print("\nHiç IP adresi bulunamadı!")
        return
    
    # IP'leri frekansa göre sırala
    sorted_ips = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    print("\n" + "+" + "-"*38 + "+")
    print("|        IP BAĞLANTI ÖZETİ        |")
    print("+" + "-"*38 + "+")
    print(f"| İşlenen satır: {analysis_data['total_lines']:10}   |")
    print(f"| Benzersiz IP:  {analysis_data['unique_ips']:10}   |")
    print("+" + "-"*38 + "+")
    
    # Detaylı liste
    print("\nDETAYLI LİSTE:")
    print("-" * 30)
    print(f"{'IP Adresi':<18} | {'Sayı':<5}")
    print("-" * 30)
    
    total_connections = sum(stats.values())
    
    for ip, count in sorted_ips:
        print(f"{ip:<18} | {count:<5}")
    
    print("-" * 30)
    print(f"Toplam bağlantı: {total_connections}")


def main():
    """Programın ana giriş noktası."""
    print("=== Log IP Analiz Aracı ===\n")
    
    # Dosya belirtilmemişse varsayılanı kullan
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = "sample.log"
        print(f"Dosya belirtilmedi, varsayılan: '{log_file}' kullanılıyor...")
    
    # Log dosyasını analiz et
    results = parse_log_file(log_file)
    
    if results:
        display_results(results)
        
        # Ekstra: En çok bağlantı yapan IP
        if results['stats']:
            max_ip = max(results['stats'].items(), key=lambda x: x[1])
            print(f"\n→ En çok bağlantı: {max_ip[0]} ({max_ip[1]} kez)")


if __name__ == "__main__":
    main()
