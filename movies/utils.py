from PIL import Image
import os
from django.conf import settings

def optimize_slider_image(image_path, target_width=1920, target_height=1080):
    """
    Slider için resimleri optimize eder:
    - Tüm resimleri aynı boyuta (1920x1080) getirir
    - En-boy oranını korur ve fazlalık kısmı kırpar
    - Resmi ortalar
    - Dosya boyutunu optimize eder
    """
    try:
        img_full_path = os.path.join(settings.BASE_DIR, image_path)
        
        if not os.path.exists(img_full_path):
            return False

        with Image.open(img_full_path) as img:
            # PNG'yi JPEG'e çevir
            if img.format == 'PNG':
                img = img.convert('RGB')
            
            # Orijinal en-boy oranı
            aspect_ratio = target_width / target_height
            original_aspect_ratio = img.width / img.height
            
            # Yeni boyutları hesapla
            if original_aspect_ratio > aspect_ratio:
                # Resim çok geniş
                new_height = target_height
                new_width = int(new_height * original_aspect_ratio)
            else:
                # Resim çok uzun
                new_width = target_width
                new_height = int(new_width / original_aspect_ratio)
            
            # Resmi yeniden boyutlandır (yüksek kalite)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Resmi ortala ve kırp
            left = (new_width - target_width) / 2
            top = (new_height - target_height) / 2
            right = (new_width + target_width) / 2
            bottom = (new_height + target_height) / 2
            
            img = img.crop((left, top, right, bottom))
            
            # Optimize edip kaydet
            img.save(img_full_path, 'JPEG', 
                    quality=85, # Kalite seviyesi
                    optimize=True, # Dosya boyutunu optimize et
                    progressive=True) # Progressive JPEG formatı
            
            return True
    except Exception as e:
        print(f"Resim optimize edilirken hata oluştu: {str(e)}")
        return False
