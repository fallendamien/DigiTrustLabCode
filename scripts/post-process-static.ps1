# Post-process static HTML files after Simply Static export
# Fixes: search bar injection, breadcrumbs, share links, shortcodes, dummy content cleanup

$staticDir = "D:\Coding Zone\digitrust-lab-static"

# --- Phase 0: Inject search bar into header (Simply Static strips form/input tags) ---
$searchBarHTML = '<div style="display:flex;align-items:center;gap:12px;"><form action="/" method="get" style="display:flex;align-items:center;position:relative;"><input type="text" name="s" placeholder="Cari..." style="border:1px solid #EBEBEB;border-radius:6px;padding:5px 12px;font-size:12px;font-family:' + "'Plus Jakarta Sans'" + ',system-ui,sans-serif;width:180px;outline:none;height:32px;box-sizing:border-box;"><button type="submit" style="background:none;border:none;cursor:pointer;position:absolute;right:8px;top:50%;transform:translateY(-50%);padding:0;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B6B6B" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg></button></form><a href="#" style="background:#E8621A;color:#fff;font-family:' + "'Plus Jakarta Sans'" + ',system-ui,sans-serif;font-size:12px;font-weight:600;padding:7px 14px;border-radius:6px;text-decoration:none;white-space:nowrap;">Dapatkan Panduan Percuma</a></div>'

Write-Host "`n--- Phase 0: Inject search bar into headers ---" -ForegroundColor Cyan
$allHtmlForSearch = Get-ChildItem $staticDir -Filter "*.html" -Recurse | Where-Object { $_.FullName -notmatch 'wp-content|wp-includes' }
$searchFixCount = 0
foreach ($file in $allHtmlForSearch) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    # Check if header has nav but is missing the search form (Simply Static strips it)
    if ($content -match 'brxe-hdr001' -and $content -notmatch 'name="s"') {
        # Replace: </nav><a href="#" style="background:#E8621A...>...</a></div></div></header>
        # With:   </nav><SEARCH_BAR_HTML</div></div></header>
        $pattern = '</nav><a href="#" style="background:#E8621A[^"]*"[^>]*>Dapatkan Panduan Percuma</a></div></div></header>'
        $content = $content -replace $pattern, "</nav>$searchBarHTML</div></div></header>"
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        $searchFixCount++
        Write-Host "  Injected search bar: $($file.Name)" -ForegroundColor Green
    }
}
Write-Host "Injected search bar into $searchFixCount files" -ForegroundColor Green

# --- Phase 2: Add breadcrumbs to post pages ---
$postPages = @(
    "simply-static-export-pipeline-will-be-deleted-after-testing"
)

# Find all post HTML files (not pages like privasi/disclaimer/hubungi/tentang)
$allHtmlFiles = Get-ChildItem $staticDir -Filter "index.html" -Recurse | Where-Object {
    $relPath = $_.FullName.Replace($staticDir, "").TrimStart('\')
    # Exclude known pages, templates, author, category, wp-content, wp-includes
    $relPath -notmatch '^(privasi|disclaimer|hubungi|tentang|template|author|category|wp-content|wp-includes|index\.html)' -and
    $relPath -notmatch 'wp-content|wp-includes'
}

Write-Host "Found $($allHtmlFiles.Count) potential post pages to process" -ForegroundColor Cyan

foreach ($file in $allHtmlFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $modified = $false

    # --- Fix share links: remove /blog/ prefix ---
    if ($content -match '%2Fblog%2F') {
        $content = $content -replace '%2Fblog%2F', '%2F'
        $modified = $true
        Write-Host "  Fixed share links in: $($file.Name)" -ForegroundColor Yellow
    }

    # --- Fix raw shortcodes ---
    # [rank_math_reading_time] -> "X min bacaan" (estimate from content)
    if ($content -match '\[rank_math_reading_time\]') {
        # Count words in the main content area
        $wordCount = ($content -replace '<[^>]+>', ' ' -replace '\s+', ' ' -split ' ').Count
        $readTime = [math]::Max(1, [math]::Round($wordCount / 200))
        $content = $content -replace '\[rank_math_reading_time\]', "$readTime min bacaan"
        $modified = $true
        Write-Host "  Fixed reading time shortcode in: $($file.Name)" -ForegroundColor Yellow
    }

    # [rank_math_toc] -> Remove (TOC needs JS, skip for now)
    if ($content -match '\[rank_math_toc\]') {
        $content = $content -replace '\[rank_math_toc\]', ''
        $modified = $true
        Write-Host "  Removed TOC shortcode in: $($file.Name)" -ForegroundColor Yellow
    }

    # --- Add breadcrumbs (if not already present) ---
    if ($content -notmatch 'dtl-breadcrumb' -and $content -match 'dtl-post-wrap') {
        $breadcrumbHTML = '<div class="dtl-breadcrumb" style="max-width:620px;margin:0 auto;padding:12px 20px 0;font-family:' + "'Plus Jakarta Sans'" + ',system-ui,sans-serif;font-size:12px;color:#6B6B6B;"><a href="/" style="color:#6B6B6B;text-decoration:none;">Beranda</a> <span style="color:#CCC;">&rsaquo;</span> <span style="color:#1A1A1A;font-weight:500;">Artikel</span></div>'
        $content = $content -replace '(<div class="dtl-post-wrap")', "$breadcrumbHTML`$1"
        $modified = $true
        Write-Host "  Added breadcrumbs to: $($file.Name)" -ForegroundColor Green
    }

    if ($modified) {
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        Write-Host "  Saved: $($file.FullName)" -ForegroundColor Green
    }
}

# --- Phase 5: Fix share links in ALL html files (including non-post pages) ---
Write-Host "`nFixing share links in all HTML files..." -ForegroundColor Cyan
$allFiles = Get-ChildItem $staticDir -Filter "*.html" -Recurse
$shareFixCount = 0
foreach ($file in $allFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    if ($content -match '/blog/' -and $content -match 'share') {
        $content = $content -replace '/blog/', '/'
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        $shareFixCount++
    }
}
Write-Host "Fixed share links in $shareFixCount files" -ForegroundColor Green

# --- Phase 6: Fix double-slash links (Simply Static replaces https://domain -> / creating //path) ---
Write-Host "`n--- Phase 6: Fix double-slash links ---" -ForegroundColor Cyan
$allFilesForSlash = Get-ChildItem $staticDir -Filter "*.html" -Recurse | Where-Object { $_.FullName -notmatch 'wp-content|wp-includes' }
$slashFixCount = 0
foreach ($file in $allFilesForSlash) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $modified = $false
    # Fix href="//path" -> href="/path" (but NOT https://)
    if ($content -match 'href="//(?!/)') {
        $content = $content -replace 'href="//(?!/)', 'href="/'
        $modified = $true
    }
    # Fix src="//path" -> src="/path" (but NOT https://)
    if ($content -match 'src="//(?!/)') {
        $content = $content -replace 'src="//(?!/)', 'src="/'
        $modified = $true
    }
    if ($modified) {
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        $slashFixCount++
        Write-Host "  Fixed double-slash: $($file.Name)" -ForegroundColor Green
    }
}
Write-Host "Fixed double-slash links in $slashFixCount files" -ForegroundColor Green

# --- Phase 7: Remove dummy post static files ---
$dummyPostPath = "$staticDir\simply-static-export-pipeline-will-be-deleted-after-testing"
if (Test-Path $dummyPostPath) {
    Remove-Item $dummyPostPath -Recurse -Force
    Write-Host "`nRemoved dummy post directory" -ForegroundColor Green
}

Write-Host "`n✅ Post-processing complete!" -ForegroundColor Green
