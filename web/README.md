# 🎓 Face Recognition Learning Platform - Web Documentation

Website pembelajaran interaktif untuk Face Recognition Attendance System (8 Minggu).

## 📁 Struktur Folder

```
web/
├── index.html              # Homepage utama
├── README.md               # Dokumentasi (file ini)
├── assets/
│   ├── css/
│   │   └── styles.css      # Styling lengkap
│   └── js/
│       └── script.js       # Interaktivitas & konten detail
```

## ✨ Fitur Website

### 1. Homepage
- **Hero Section** dengan call-to-action buttons
- **Overview** project dengan fitur-fitur utama
- **Tech Stack** visual grid
- **Quick Start** guides (3 learning paths)

### 2. Learning Path (8 Minggu)
- **Week Cards** dengan difficulty indicators
- **Interactive Modals** - klik setiap minggu untuk detail lengkap:
  - Objectives & learning goals
  - Tutorial topics per file
  - Module functions & API
  - Key concepts & architecture
  - Commands untuk menjalankan
  - Database schema (Week 6)
  - GUI windows (Week 7)
  - Distribution options (Week 8)

### 3. Navigation
- **Sticky navbar** dengan smooth scrolling
- **Active state** tracking saat scroll
- **Responsive** untuk mobile & desktop

### 4. Content
Website ini menjelaskan **semua materi minggu 1-8**:
- ✅ Minggu 1: Python Basics & OpenCV (5 tutorials)
- ✅ Minggu 2: Face Detection (4 tutorials)
- ✅ Minggu 3: Face Recognition (3 tutorials)
- ✅ Minggu 4: Dataset & Database (2 tutorials)
- ✅ Minggu 5: Hybrid Recognition System (2 tutorials)
- ✅ Minggu 6: Attendance System (2 tutorials)
- ✅ Minggu 7: Desktop GUI (2 tutorials)
- ✅ Minggu 8: Final Testing & Distribution (3 tutorials)

**Total: 25 tutorials dijelaskan dengan detail!**

## 🚀 Cara Menjalankan

### Option 1: Simple HTTP Server (Python)
```powershell
cd web
python -m http.server 8000
```
Buka browser: `http://localhost:8000`

### Option 2: Live Server (VS Code Extension)
1. Install extension "Live Server" di VS Code
2. Right-click `index.html` → "Open with Live Server"
3. Browser otomatis terbuka

### Option 3: Langsung Buka File
Double-click `index.html` di File Explorer (works tapi relative paths mungkin bermasalah)

## 💡 Cara Menggunakan Website

1. **Scroll** atau klik navigation menu untuk jelajahi sections
2. **Klik "Lihat Detail →"** pada week card untuk membuka modal dengan penjelasan lengkap
3. **Modal berisi**:
   - Tujuan pembelajaran
   - Topik & tutorial files
   - Module functions (API reference)
   - Key concepts
   - Commands untuk run
   - Architecture diagram (Week 5)
   - Database schema (Week 6)
   - GUI windows (Week 7)
   - PyInstaller commands (Week 8)
4. **Close modal**: klik X, klik di luar modal, atau tekan ESC

## 🎨 Design Features

### Color Scheme
- **Primary**: Blue (#3b82f6)
- **Secondary**: Purple (#8b5cf6)
- **Success**: Green (#10b981)
- **Text**: Dark gray (#1f2937)
- **Background**: White & light gray

### Responsive Design
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

### Animations
- Smooth scrolling
- Fade in on page load
- Hover effects pada cards
- Slide in animation untuk modal

## 📝 Customization

### Menambah/Edit Konten Week
Edit file `assets/js/script.js`, section `weekDetails`:

```javascript
const weekDetails = {
    1: {
        title: "...",
        objectives: [...],
        topics: [...],
        // etc
    }
}
```

### Mengubah Warna
Edit file `assets/css/styles.css`, section `:root`:

```css
:root {
    --primary: #3b82f6;
    --secondary: #8b5cf6;
    /* etc */
}
```

### Menambah Section Baru
Edit `index.html`, tambahkan section baru:

```html
<section id="new-section" class="section">
    <div class="container">
        <h2>Section Baru</h2>
        <!-- content -->
    </div>
</section>
```

Update navigation di `<nav>`:
```html
<li><a href="#new-section" class="nav-link">Section Baru</a></li>
```

## 🛠️ Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Modern styling (Grid, Flexbox, CSS Variables)
- **Vanilla JavaScript** - No frameworks/dependencies
- **Responsive Design** - Mobile-first approach

## 📱 Browser Support

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ⚠️ IE11 (partial support)

## 🎯 Use Cases

1. **Self-learning** - Baca materi week-by-week
2. **Quick reference** - Cari konsep/commands tertentu
3. **Teaching** - Present materi dengan visual menarik
4. **Portfolio** - Showcase learning journey
5. **Documentation** - Reference untuk troubleshooting

## 📦 Deployment Options

### Option 1: GitHub Pages (Free)
```bash
# Push ke GitHub
git add web/
git commit -m "Add learning website"
git push origin main

# Settings → Pages → Source: main branch / web folder
```
URL: `https://username.github.io/repo-name/`

### Option 2: Netlify/Vercel (Free)
1. Drag & drop folder `web/` ke dashboard
2. Site langsung live!

### Option 3: Hosting Tradisional
Upload folder `web/` ke public_html via FTP

## 🐛 Troubleshooting

**Modal tidak muncul?**
- Check browser console untuk errors
- Pastikan `script.js` loaded correctly

**Styling berantakan?**
- Pastikan `styles.css` path benar di `index.html`
- Clear browser cache (Ctrl+Shift+R)

**Smooth scroll tidak jalan?**
- Pastikan browser support `scroll-behavior: smooth`
- Fallback: JavaScript smooth scroll sudah implemented

## ✅ Checklist Fitur

- [x] Homepage dengan hero section
- [x] Navigation dengan smooth scrolling
- [x] Overview section (cards)
- [x] Tech stack section
- [x] Learning path (8 week cards)
- [x] Quick start guides
- [x] Interactive modals untuk setiap week
- [x] Detailed content (25 tutorials explained)
- [x] Responsive design (mobile/tablet/desktop)
- [x] Keyboard navigation (ESC untuk close modal)
- [x] Accessibility (semantic HTML)
- [x] Performance (vanilla JS, no bloat)

## 🎉 Summary

Website ini adalah **learning platform interaktif** yang menjelaskan **SEMUA materi minggu 1-8** dalam format yang:
- 📚 **Lengkap**: 25 tutorials, modules, concepts dijelaskan
- 🎨 **Visual**: Clean design, cards, modals
- 📱 **Responsive**: Works di semua devices
- ⚡ **Fast**: No external dependencies
- 🎯 **Focused**: Easy navigation, clear structure

**Perfect untuk:**
- Students yang sedang belajar
- Instructors untuk teaching material
- Portfolio showcase
- Quick reference guide

---

**Enjoy learning! 🚀**

Last Updated: November 14, 2025
