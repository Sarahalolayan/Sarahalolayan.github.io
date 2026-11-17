# Builds the four Arabic service pages (/services/<slug>/) and the English page (/en/).
# Run: python _src/build_pages.py   (folders starting with "_" are not published by GitHub Pages)
import os, json, html, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://sarahalolayan.github.io'
WA = '966557912466'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&family=Readex+Pro:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">')
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2308131d'/%3E%3Cpath d='M9 25 L16 8 L23 25' fill='none' stroke='%239ad6c8' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E"
MARK = '<span class="mark" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 17 L10 3.5 L16 17"/><circle cx="7" cy="12.2" r="1.6" fill="currentColor" stroke="none"/><circle cx="13" cy="12.2" r="1.6" fill="currentColor" stroke="none"/><path d="M8.6 12.2 H11.4" stroke-width="1.6"/></svg></span>'
MOON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>'
BURGER = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
WA_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.7-5.3A8.4 8.4 0 1 1 21 11.5z"/></svg>'
ICONS = {
 'dash': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 'auto': '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H14a4 4 0 0 1 4 4v5.5"/>',
 'web': '<rect x="3" y="4" width="18" height="15" rx="2"/><path d="M3 8.5h18"/><path d="M8 13h5"/>',
 'org': '<rect x="3" y="4" width="7" height="6" rx="1.5"/><rect x="14" y="14" width="7" height="6" rx="1.5"/><path d="M6.5 10v4a3 3 0 0 0 3 3H14"/>',
 'bell': '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>',
 'doc': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',
 'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 'phone': '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>',
 'chat': '<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.7-5.3A8.4 8.4 0 1 1 21 11.5z"/>',
 'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 'eye': '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
}
def icon(k, size=18): return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>'
def wa(msg): return f'https://wa.me/{WA}?text=' + urllib.parse.quote(msg)
esc = html.escape

# hero illustrations, drawn once per service
ART = {
 'dashboards': '''<svg viewBox="0 0 320 190" aria-hidden="true"><rect x="10" y="10" width="300" height="170" rx="12" fill="var(--sunk)" stroke="var(--line)"/>
  <rect x="24" y="24" width="84" height="44" rx="8" fill="var(--surface)" stroke="var(--line)"/><text x="98" y="42" text-anchor="end" font-size="10" fill="var(--muted)" font-family="IBM Plex Sans Arabic">المبيعات</text><text x="98" y="60" text-anchor="end" font-size="15" fill="var(--ink)" font-family="IBM Plex Mono">48,210</text>
  <rect x="118" y="24" width="84" height="44" rx="8" fill="var(--surface)" stroke="var(--line)"/><text x="192" y="42" text-anchor="end" font-size="10" fill="var(--muted)" font-family="IBM Plex Sans Arabic">الطلبات</text><text x="192" y="60" text-anchor="end" font-size="15" fill="var(--ink)" font-family="IBM Plex Mono">265</text>
  <rect x="212" y="24" width="84" height="44" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="286" y="42" text-anchor="end" font-size="10" fill="var(--ink-2)" font-family="IBM Plex Sans Arabic">مقارنة بأمس</text><text x="286" y="60" text-anchor="end" font-size="15" fill="var(--accent)" font-family="IBM Plex Mono">▲ 12%</text>
  <g fill="var(--accent)" opacity=".8"><rect x="34" y="128" width="20" height="38" rx="3"/><rect x="66" y="112" width="20" height="54" rx="3"/><rect x="98" y="120" width="20" height="46" rx="3"/><rect x="130" y="98" width="20" height="68" rx="3"/><rect x="162" y="106" width="20" height="60" rx="3"/><rect x="194" y="88" width="20" height="78" rx="3"/><rect x="226" y="94" width="20" height="72" rx="3" opacity=".5"/></g>
  <path fill="none" d="M44 120 L76 104 L108 112 L140 90 L172 98 L204 80 L276 84" fill="none" stroke="var(--ink-2)" stroke-width="2" stroke-dasharray="4 4"/><circle cx="276" cy="84" r="5" fill="var(--accent)"/></svg>''',
 'automation': '''<svg viewBox="0 0 320 190" aria-hidden="true"><rect x="10" y="10" width="300" height="170" rx="12" fill="var(--sunk)" stroke="var(--line)"/>
  <path d="M236 70 H180 M128 70 H84" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="5 6"/><path d="M154 92 V130 H112" fill="none" stroke="var(--line)" stroke-width="2.5"/>
  <rect x="236" y="46" width="60" height="48" rx="10" fill="var(--surface)" stroke="var(--accent)"/><text x="266" y="74" text-anchor="middle" font-size="11" fill="var(--ink)" font-family="IBM Plex Sans Arabic">طلب جديد</text>
  <rect x="128" y="46" width="52" height="48" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="154" y="74" text-anchor="middle" font-size="11" fill="var(--ink)" font-family="IBM Plex Sans Arabic">شرط</text>
  <rect x="24" y="46" width="60" height="48" rx="10" fill="var(--surface)" stroke="var(--accent)"/><text x="54" y="74" text-anchor="middle" font-size="11" fill="var(--ink)" font-family="IBM Plex Sans Arabic">تنبيه</text>
  <rect x="52" y="112" width="60" height="38" rx="10" fill="var(--surface)" stroke="var(--line)"/><text x="82" y="135" text-anchor="middle" font-size="11" fill="var(--ink-2)" font-family="IBM Plex Sans Arabic">تقرير</text>
  <circle r="5" fill="var(--accent)"><animateMotion dur="1.8s" repeatCount="indefinite" path="M236 70 H180"/></circle><circle r="5" fill="var(--accent)"><animateMotion dur="1.8s" begin=".9s" repeatCount="indefinite" path="M128 70 H84"/></circle>
  <text x="160" y="168" text-anchor="middle" font-size="11" fill="var(--muted)" font-family="IBM Plex Sans Arabic">تُنفّذ وحدها خلال ثوانٍ</text></svg>''',
 'websites': '''<svg viewBox="0 0 320 190" aria-hidden="true"><defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FB0C4"/><stop offset="1" stop-color="#2F5560"/></linearGradient></defs>
  <rect x="60" y="10" width="250" height="160" rx="12" fill="var(--surface)" stroke="var(--line)"/><circle cx="76" cy="24" r="3.5" fill="var(--line)"/><circle cx="88" cy="24" r="3.5" fill="var(--line)"/><circle cx="100" cy="24" r="3.5" fill="var(--line)"/>
  <rect x="70" y="36" width="230" height="84" rx="6" fill="url(#sk)"/><path d="M70 120 V100 Q120 76 170 96 T260 88 Q282 84 300 94 V120 Z" fill="#24443F" opacity=".85"/>
  <rect x="200" y="54" width="86" height="9" rx="4.5" fill="#fff" opacity=".9"/><rect x="226" y="70" width="60" height="7" rx="3.5" fill="#fff" opacity=".6"/>
  <rect x="200" y="132" width="86" height="22" rx="11" fill="var(--accent)"/><text x="243" y="147" text-anchor="middle" font-size="11" fill="var(--accent-ink)" font-family="IBM Plex Sans Arabic" font-weight="600">احجز الآن</text>
  <rect x="84" y="136" width="56" height="7" rx="3.5" fill="var(--line)"/><rect x="84" y="148" width="40" height="7" rx="3.5" fill="var(--line)"/>
  <rect x="10" y="60" width="62" height="118" rx="10" fill="var(--surface)" stroke="var(--line)"/><rect x="18" y="72" width="46" height="40" rx="4" fill="url(#sk)"/><rect x="18" y="120" width="46" height="6" rx="3" fill="var(--line)"/><rect x="18" y="154" width="46" height="14" rx="7" fill="var(--accent)"/></svg>''',
 'process': '''<svg viewBox="0 0 320 190" aria-hidden="true"><rect x="10" y="10" width="300" height="170" rx="12" fill="var(--sunk)" stroke="var(--line)"/>
  <path d="M276 95 H238 M186 95 H168 M140 95 H124 V60 H104 M124 95 V130 H104 M58 60 H40 V95 M58 130 H40 V95 H30" fill="none" stroke="var(--line)" stroke-width="2.5"/>
  <circle cx="286" cy="95" r="11" fill="var(--surface)" stroke="var(--accent)" stroke-width="2.5"/>
  <rect x="186" y="76" width="52" height="38" rx="8" fill="var(--surface)" stroke="var(--line)"/><text x="212" y="99" text-anchor="middle" font-size="11" fill="var(--ink)" font-family="IBM Plex Sans Arabic">طلب</text>
  <path d="M154 79 L170 95 L154 111 L138 95 Z" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <rect x="58" y="44" width="46" height="32" rx="8" fill="var(--surface)" stroke="var(--line)"/><text x="81" y="64" text-anchor="middle" font-size="11" fill="var(--ink)" font-family="IBM Plex Sans Arabic">موافقة</text>
  <rect x="58" y="114" width="46" height="32" rx="8" fill="var(--surface)" stroke="var(--line)"/><text x="81" y="134" text-anchor="middle" font-size="11" fill="var(--ink)" font-family="IBM Plex Sans Arabic">تعديل</text>
  <circle cx="24" cy="95" r="9" fill="var(--surface)" stroke="var(--ink-2)" stroke-width="3.5"/>
  <circle r="5" fill="var(--accent)"><animateMotion dur="4s" repeatCount="indefinite" path="M286 95 H212 H154 H124 V60 H81 H40 V95 H24"/></circle></svg>''',
}

STEPS = [('جلسة فهم', 'نفهم نشاطك والمشكلة التي تريد حلها.'), ('تصميم الحل', 'نعرض عليك الشكل والخطوات قبل البناء.'),
         ('البناء والاختبار', 'نبني ونختبر على بياناتك الفعلية.'), ('التشغيل والدعم', 'نطلق وندرّب فريقك ونتابع بعد الإطلاق.')]

SERVICES = [
 dict(slug='dashboards', icon='dash', name='شاشات متابعة الأرقام',
   title='شاشات متابعة الأرقام | Agentiq',
   desc='شاشة متابعة حية لمبيعاتك وطلباتك وأهم أرقام عملك، تتحدّث تلقائياً من أنظمتك وترسل لك تنبيهاً وملخصاً يومياً.',
   h1='أرقام عملك في شاشة واحدة، تتحدّث وحدها',
   lead='نربط الأنظمة التي تستخدمها اليوم، ونعرض أهم أرقامك مع مقارنتها بالأمس وبالهدف، ونرسل لك تنبيهاً فور حدوث أي خلل.',
   fit=['تجمع الأرقام من عدة ملفات أو أنظمة كل يوم', 'تكتشف انخفاض المبيعات أو نفاد المخزون بعد فوات الأوان', 'تريد أن ترى أداء الفروع أو الموظفين في مكان واحد', 'تحتاج تقريراً يومياً بدون أن يكتبه أحد'],
   gets=[('dash', 'شاشة تتحدّث تلقائياً', 'من Excel أو المتجر أو نظام نقاط البيع، بدون إدخال يدوي.'), ('bell', 'تنبيهات فورية', 'رسالة على جوالك عند انخفاض رقم مهم أو تجاوزه حداً تختاره.'),
         ('doc', 'ملخص يومي مكتوب', 'تقرير قصير يصلك آخر كل يوم بما حدث وما يحتاج انتباهك.'), ('eye', 'صلاحيات عرض', 'كل شخص يرى الأرقام التي تخصه فقط.')],
   uses=['مبيعات المتجر الإلكتروني والطلبات والمخزون', 'حضور العملاء في نادٍ أو عيادة أو مركز تدريب', 'أداء الفروع ومقارنتها ببعض', 'متابعة فريق المبيعات والأهداف الشهرية'],
   example=('مشروع منشور', 'نبض النادي', 'شاشة لنادٍ رياضي فيها عدد المتدربين ومقارنتهم بالهدف، وتنبيهات وملخص يومي.', SITE + '/nabd-alnadi/', 'افتح الشاشة ↗'),
   faq=[('من أين تأتي الأرقام؟', 'من الأنظمة التي تستخدمها حالياً: ملفات Excel أو Google Sheets، متجر سلة أو زد، نظام نقاط البيع، أو قاعدة بيانات.'),
        ('هل أحتاج جهازاً أو برنامجاً خاصاً؟', 'لا. الشاشة تفتح من المتصفح على الكمبيوتر أو الجوال.'),
        ('كم مرة تتحدّث الأرقام؟', 'حسب حاجتك: كل دقيقة، أو كل ساعة، أو مرة يومياً.')]),
 dict(slug='automation', icon='auto', name='أتمتة المهام المتكررة',
   title='أتمتة المهام المتكررة | Agentiq',
   desc='نجعل المهام اليومية المتكررة تُنجز وحدها: نقل البيانات بين الأنظمة، التقارير المجدولة، الطلبات والموافقات، والتنبيهات.',
   h1='المهام التي تكررها كل يوم، تُنجز وحدها',
   lead='أي مهمة لها نفس الخطوات كل مرة يمكن أن تعمل تلقائياً: تسجيل الطلبات، نسخ البيانات، إعداد التقارير، ومتابعة الموافقات.',
   fit=['فريقك ينسخ البيانات من نظام إلى آخر يدوياً', 'يكتب أحدهم تقريراً بنفس الشكل كل يوم أو أسبوع', 'الطلبات والموافقات تضيع بين الرسائل والأوراق', 'تريد تنبيهاً تلقائياً عند حدوث شيء معين'],
   gets=[('link', 'ربط أنظمتك ببعض', 'المتجر وExcel والبريد وواتساب ونظامك الداخلي تتبادل البيانات وحدها.'), ('doc', 'تقارير في موعدها', 'تُجمع وتُكتب وتُرسل تلقائياً بدون تدخل.'),
         ('cal', 'طلبات وموافقات إلكترونية', 'الطلب يصل للمدير ويعود بالرد، ويُسجّل كل شيء.'), ('bell', 'تنبيهات بشروطك', 'أنت تحدد متى يُرسل التنبيه ولمن.')],
   uses=['طلب جديد في المتجر يُسجّل في الشيت وينبّه المدير عند نقص المخزون', 'تقرير مبيعات أسبوعي يصل للإدارة كل أحد', 'طلب إجازة يمر بالموافقة ويُبلغ الموظف تلقائياً', 'فاتورة جديدة تُسجّل في دفتر الحسابات'],
   example=('مثال تفاعلي', 'ثلاث مهام تُنجز وحدها', 'شغّل المحاكي وشاهد كل خطوة تُنفّذ: طلب متجر، تقرير يومي، وطلب إجازة.', SITE + '/#lab', 'شغّل المحاكي ←'),
   faq=[('كيف أعرف أي مهامي تستحق الأتمتة؟', 'استخدم حاسبة تكلفة الأعمال اليدوية في موقعنا، أو نحددها معك في جلسة الفهم.'),
        ('هل تتوقف الأتمتة إذا تغيّر شيء؟', 'نراقبها ونرسل تنبيهاً عند أي خطأ، ونعدّلها إذا تغيّرت طريقة عملك.'),
        ('هل يحتاج فريقي تدريباً؟', 'تدريب قصير فقط، لأن أغلب الأتمتة تعمل في الخلفية بدون تدخل.')]),
 dict(slug='websites', icon='web', name='المواقع الإلكترونية وصفحات الحجز',
   title='مواقع إلكترونية وصفحات حجز | Agentiq',
   desc='مواقع عربية سريعة بتصميم خاص، تعمل على الجوال، مع معرض أعمال ونموذج حجز أو طلب سعر يصلك على واتساب.',
   h1='موقع يعرض نشاطك ويحوّل الزائر إلى طلب',
   lead='نصمم موقعاً عربياً سريعاً بهويتك، يعمل على الجوال قبل الكمبيوتر، ويوصل لك طلبات الحجز والأسعار جاهزة على واتساب.',
   fit=['ليس لديك موقع، أو موقعك قديم ولا يعمل جيداً على الجوال', 'تصلك الطلبات متفرقة في الرسائل بدون تفاصيل', 'تريد معرضاً لأعمالك أو منتجاتك يمكنك مشاركته', 'تحتاج صفحة واحدة لحملة إعلانية'],
   gets=[('web', 'تصميم خاص بهويتك', 'بدون قوالب مكررة، بألوانك وخطوطك.'), ('phone', 'يعمل على الجوال أولاً', 'لأن أغلب زوارك يفتحون من الجوال.'),
         ('chat', 'حجز وطلب سعر عبر واتساب', 'نموذج يجمع التفاصيل ويرسلها لك جاهزة.'), ('eye', 'معرض لأعمالك', 'صور وأمثلة تعرض جودة عملك.')],
   uses=['استديو تصوير مع معرض أعمال ونموذج حجز جلسة', 'مطعم أو مقهى مع المنيو ورابط الطلب', 'عيادة أو مركز مع حجز موعد', 'صفحة هبوط لحملة إعلانية'],
   example=('نموذج لعميل', 'موقع استديو تصوير', 'عدسة تنفتح مع التمرير، ومعرض أعمال بصور كاملة الشاشة، ونموذج حجز يرسل الطلب على واتساب.', SITE + '/demos/bahrawi/', 'افتح الموقع ↗'),
   faq=[('هل يمكنني تعديل المحتوى بنفسي؟', 'نعم، نسلّمك طريقة بسيطة لتعديل النصوص والصور، أو نتولى التعديلات عنك.'),
        ('هل يظهر الموقع في بحث Google؟', 'نجهّز الموقع بأساسيات الظهور في محركات البحث وصورة المشاركة في وسائل التواصل.'),
        ('هل تربطون دومين باسمي؟', 'نعم، نربط الموقع بالدومين الذي تختاره.')]),
 dict(slug='process', icon='org', name='تنظيم الإجراءات والصلاحيات',
   title='تنظيم الإجراءات والصلاحيات | Agentiq',
   desc='نوثّق خطوات العمل ونبسّطها، ونحدد من يرى ماذا من البيانات، ونتابع الالتزام بتقارير دورية، قبل أي أتمتة.',
   h1='طريقة عمل واضحة، يعرف فيها كل شخص دوره',
   lead='قبل أتمتة أي شيء نرتّب طريقة العمل نفسها: نوثّق الخطوات، ونكتشف التأخير والتكرار، ونضع قواعد واضحة للصلاحيات والبيانات.',
   fit=['الفريق يكبر والمهام تتداخل', 'كل موظف ينجز نفس المهمة بطريقة مختلفة', 'لا تعرف بالضبط من يستطيع رؤية أو تعديل بيانات العملاء', 'تحتاج تجهيز عملك لمراجعة أو تدقيق'],
   gets=[('doc', 'خطوات عمل موثقة', 'مكتوبة ومرسومة بشكل يفهمه الجميع.'), ('org', 'إجراءات أبسط', 'نحذف الخطوات المكررة ونقصّر مسار الطلبات.'),
         ('lock', 'قواعد الصلاحيات', 'من يرى ماذا، ومن يعدّل ماذا، في كل نظام.'), ('eye', 'متابعة الالتزام', 'تقارير دورية بما تم وما يحتاج تصحيحاً.')],
   uses=['توثيق إجراء استقبال العملاء من أول تواصل حتى التسليم', 'سياسة صلاحيات الموظفين على الأنظمة والبيانات', 'تبسيط مسار الطلبات والموافقات الداخلية', 'تقارير متابعة الالتزام للإدارة'],
   example=('من خبرة الفريق', 'من يرى ماذا من البيانات', 'قواعد واضحة لصلاحيات الموظفين على الأنظمة، ومتابعة الالتزام بها بتقارير دورية.', SITE + '/#work', 'شاهد أعمالنا ←'),
   faq=[('هل هذه الخدمة لشركات كبيرة فقط؟', 'لا. حتى فريق من خمسة أشخاص يستفيد من خطوات واضحة وصلاحيات محددة.'),
        ('ما الذي أستلمه في النهاية؟', 'وثيقة الإجراءات، ورسومات خطوات العمل، وقواعد الصلاحيات، وخطة متابعة.'),
        ('هل يمكن أتمتة الإجراءات بعد تنظيمها؟', 'نعم، وهذه أفضل نقطة بداية للأتمتة.')]),
]

def head(lang, title, desc, path, alt_path=None, extra=''):
    d = 'rtl' if lang == 'ar' else 'ltr'
    alts = ''
    if alt_path:
        ar, en = (path, alt_path) if lang == 'ar' else (alt_path, path)
        alts = f'<link rel="alternate" hreflang="ar" href="{SITE}{ar}"><link rel="alternate" hreflang="en" href="{SITE}{en}"><link rel="alternate" hreflang="x-default" href="{SITE}{ar}">'
    return f'''<!doctype html>
<html lang="{lang}" dir="{d}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}{path}">{alts}
<meta name="theme-color" content="#08131d">
<link rel="icon" href="{FAVICON}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Agentiq"><meta property="og:locale" content="{'ar_SA' if lang=='ar' else 'en_US'}">
<meta property="og:url" content="{SITE}{path}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/og.png"><meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/agentiq-config.js" defer></script>
{extra}
</head>
<body>'''

def nav_ar(current=''):
    items = [('/#services', 'الخدمات'), ('/#work', 'أعمالنا'), ('/hours/', 'احسب التوفير'), ('/#faq', 'الأسئلة')]
    links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in items)
    return f'''<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<nav class="nav"><div class="wrap nav-in">
  <a class="brand" href="/" aria-label="Agentiq، الصفحة الرئيسية">{MARK}<span lang="en">Agentiq</span></a>
  <div class="links" id="links">{links}</div>
  <div class="nav-r"><a class="lang" href="/en/" lang="en" hreflang="en">EN</a><a class="btn primary sm" href="/#contact">ابدأ مشروعك</a>
    <button class="icon-btn" id="theme" type="button" aria-label="تبديل الوضع الفاتح والداكن">{MOON}</button>
    <button class="icon-btn menu-btn" id="menu" type="button" aria-label="القائمة" aria-expanded="false" aria-controls="links">{BURGER}</button></div>
</div></nav>'''

def foot_ar():
    return f'''<footer class="wrap"><span>© <span class="num" id="year">2026</span> <span lang="en">Agentiq</span></span><span><a href="/">الرئيسية</a> · <a href="/hours/">حاسبة التوفير</a> · <a href="/en/" lang="en">English</a></span></footer>
<a class="fab" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="تواصل معنا عبر واتساب">{WA_ICON}<span>واتساب</span></a>
<script src="/assets/site.js" defer></script>
</body></html>
'''

def service_page(sv):
    path = f'/services/{sv["slug"]}/'
    ld = {"@context": "https://schema.org", "@type": "Service", "name": sv['name'], "description": sv['desc'], "areaServed": "SA",
          "provider": {"@type": "Organization", "name": "Agentiq", "url": SITE + "/"}, "url": SITE + path}
    msg = f'السلام عليكم، أرغب بخدمة «{sv["name"]}» من Agentiq.'
    fit = ''.join(f'<li>{esc(x)}</li>' for x in sv['fit'])
    gets = ''.join(f'<div class="tile"><h3><span class="ic">{icon(k)}</span>{esc(t)}</h3><p>{esc(p)}</p></div>' for k, t, p in sv['gets'])
    uses = ''.join(f'<li>{esc(x)}</li>' for x in sv['uses'])
    steps = ''.join(f'<li><span class="n">0{i+1}</span><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(STEPS))
    faq = ''.join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in sv['faq'])
    ex_tag, ex_title, ex_text, ex_url, ex_cta = sv['example']
    ext = ' target="_blank" rel="noopener"' if ex_cta.endswith('↗') else ''
    others = ''.join(f'<a href="/services/{o["slug"]}/"><b>{esc(o["name"])}</b><small>{esc(o["h1"])}</small></a>' for o in SERVICES if o is not sv)
    return head('ar', sv['title'], sv['desc'], path, extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>') + nav_ar() + f'''
<main class="wrap" id="main" tabindex="-1">
  <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><a href="/#services">الخدمات</a><span aria-hidden="true">›</span><span aria-current="page">{esc(sv["name"])}</span></nav>
  <header class="page-hero">
    <div class="txt">
      <span class="eyebrow">{icon(sv["icon"], 16)} {esc(sv["name"])}</span>
      <h1>{esc(sv["h1"])}</h1>
      <p>{esc(sv["lead"])}</p>
      <div class="cta-row"><a class="btn primary" href="{wa(msg)}" target="_blank" rel="noopener">اطلب هذه الخدمة عبر واتساب</a><a class="btn" href="{ex_url}"{ext}>شاهد مثالاً</a></div>
    </div>
    <div class="hero-card">{ART[sv["slug"]]}<span class="cap">مثال توضيحي</span></div>
  </header>

  <section class="block"><div class="block-head"><h2>تناسبك هذه الخدمة إذا</h2></div><ul class="checks">{fit}</ul></section>
  <section class="block"><div class="block-head"><h2>ماذا تستلم</h2></div><div class="grid g4">{gets}</div></section>
  <section class="block"><div class="block-head"><h2>أمثلة على ما نبنيه</h2></div><ul class="checks">{uses}</ul>
    <div class="example"><div><small>{esc(ex_tag)}</small><h3>{esc(ex_title)}</h3><p>{esc(ex_text)}</p></div><a class="btn" href="{ex_url}"{ext}>{ex_cta}</a></div></section>
  <section class="block"><div class="block-head"><h2>كيف نعمل</h2><p>أربع مراحل، ولكل مرحلة مخرج واضح تراجعه قبل الانتقال للتالية.</p></div><ol class="steps">{steps}</ol></section>
  <section class="block"><div class="block-head"><h2>أسئلة عن هذه الخدمة</h2></div><div class="faqs">{faq}</div></section>

  <div class="band"><div><h2>جاهز نبدأ؟</h2><p>أرسل لنا وصفاً قصيراً لما تحتاجه، ونرجع لك بتصور أولي وخطوات التنفيذ.</p></div>
    <div class="cta-row"><a class="btn" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}تواصل عبر واتساب</a><a class="btn ghost" href="/hours/">احسب كم توفّر</a></div></div>

  <section class="block"><div class="block-head"><h2>خدمات أخرى</h2></div><div class="others">{others}</div></section>
</main>
''' + foot_ar()

# ---------------- English page ----------------
EN_SERVICES = [
 ('dash', 'Live dashboards', 'Your sales, orders and key numbers on one screen that updates itself.', 'You track sales, orders or attendance every day.', ['Updates automatically from your systems', 'Compared with yesterday and with your target', 'Instant alerts and a written daily summary'], '/services/dashboards/'),
 ('auto', 'Automation of repetitive tasks', 'Any task your team repeats with the same steps can run on its own.', 'Your team copies data, writes reports or chases approvals by hand.', ['Data moves between your systems on its own', 'Reports reach you on WhatsApp or email on time', 'Electronic requests and approvals'], '/services/automation/'),
 ('web', 'Websites and booking pages', 'A fast Arabic website that works on mobile first and turns visitors into requests.', 'You need an online presence that brings bookings and quotes.', ['Custom design in your brand', 'Portfolio of your work or products', 'Booking or quote form delivered to WhatsApp'], '/services/websites/'),
 ('org', 'Process and access design', 'Clear steps and clear access rules, before anything gets automated.', 'Your team is growing and tasks and access overlap.', ['Documented and simplified workflows', 'Clear rules on who sees which data', 'Regular compliance reports'], '/services/process/'),
]
EN_WORK = [
 ('Website · client sample', 'Photography studio website', 'A lens that opens as you scroll, a full-screen gallery, studio services and a booking form that sends the quote request to WhatsApp.', SITE + '/demos/bahrawi/'),
 ('Dashboard · live project', 'Gym pulse', 'A gym dashboard showing today\'s visitors against target, with alerts and a daily summary, built on 973 real workout sessions.', SITE + '/nabd-alnadi/'),
 ('Automation · interactive demo', 'Three tasks that run themselves', 'A store order logged and flagged to the manager, a daily report sent on time, and a leave request routed for approval.', SITE + '/#lab'),
]
EN_FAQ = [
 ('Do I need a technical team?', 'No. We build and connect everything; your team just uses the result.'),
 ('Where does the data come from?', 'From the systems you already use: Excel or Google Sheets, your online store (Salla, Zid), point of sale, or a database.'),
 ('How do you protect data?', 'Each user gets only the access they need, and the data stays yours.'),
 ('How long does a project take?', 'It depends on the scope. We set the timeline after the discovery session, before any work starts.'),
 ('Can I start small?', 'Yes. Start with one dashboard or one automated task, then grow.'),
 ('Do you work in English?', 'Yes. We work in Arabic and English. Most of our live samples are in Arabic.'),
]
def en_page():
    path = '/en/'
    msg = 'Hello, I would like to discuss a project with Agentiq.'
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Agentiq", "url": SITE + "/en/", "telephone": "+" + WA, "areaServed": "SA",
          "description": "Live dashboards, automation of repetitive tasks, websites with booking forms, and process design."}
    svc = ''.join(f'''<article class="tile"><h3><span class="ic">{icon(k)}</span>{t}</h3><p>{p}</p><p style="font-size:14px;color:var(--ink)"><b style="color:var(--accent)">Good fit if</b> {fit}</p>
      <ul class="checks" style="font-size:14px">{''.join(f"<li>{x}</li>" for x in gets)}</ul><a href="{url}" hreflang="ar" style="font-weight:500;text-decoration:none">Details (Arabic) →</a></article>''' for k, t, p, fit, gets, url in EN_SERVICES)
    work = ''.join(f'<div class="example"><div><small>{tag}</small><h3>{t}</h3><p>{d}</p></div><a class="btn" href="{u}"{" target=\"_blank\" rel=\"noopener\"" if "#" not in u else ""}>Open{" ↗" if "#" not in u else " →"}</a></div>' for tag, t, d, u in EN_WORK)
    steps_en = [('Discovery', 'We learn your business and the numbers that matter.'), ('Design', 'You approve the screens, alerts and reports before we build.'), ('Build & test', 'We build and test on your real data.'), ('Launch & support', 'We launch, train your team and stay on for changes.')]
    steps = ''.join(f'<li><span class="n">0{i+1}</span><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(steps_en))
    faq = ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in EN_FAQ)
    return head('en', 'Agentiq | Live dashboards, automation and websites', 'Agentiq builds live dashboards for your business numbers, automates repetitive tasks, and designs websites with booking forms. Based in Riyadh, Saudi Arabia.', path, alt_path='/',
                extra=f'<script type="application/ld+json">{json.dumps(ld)}</script>') + f'''
<a class="skip" href="#main">Skip to content</a>
<nav class="nav"><div class="wrap nav-in">
  <a class="brand" href="/en/" aria-label="Agentiq home">{MARK}<span>Agentiq</span></a>
  <div class="links" id="links"><a href="#services">Services</a><a href="#work">Work</a><a href="#how">How we work</a><a href="#faq">FAQ</a></div>
  <div class="nav-r"><a class="lang" href="/" lang="ar" hreflang="ar">عربي</a><a class="btn primary sm" href="#contact">Start a project</a>
    <button class="icon-btn" id="theme" type="button" aria-label="Toggle light and dark mode">{MOON}</button>
    <button class="icon-btn menu-btn" id="menu" type="button" aria-label="Menu" aria-expanded="false" aria-controls="links">{BURGER}</button></div>
</div></nav>
<main class="wrap" id="main" tabindex="-1">
  <header class="page-hero">
    <div class="txt">
      <span class="eyebrow">Dashboards · Automation · Websites</span>
      <h1>Your numbers in front of you. Your repetitive work done automatically.</h1>
      <p>We connect the systems you already use, show your key numbers on one screen that updates itself, and send you alerts and ready-made reports instead of chasing them by hand.</p>
      <div class="cta-row"><a class="btn primary" href="#contact">Start a project</a><a class="btn" href="#work">See our work</a></div>
    </div>
    <div class="hero-card">{ART["dashboards"]}<span class="cap">Illustrative example (Arabic interface)</span></div>
  </header>

  <section class="block" id="services"><div class="block-head"><h2>Services</h2><p>Four services that work together. Start with one and grow.</p></div><div class="grid g2">{svc}</div></section>
  <section class="block" id="work"><div class="block-head"><h2>Our work</h2><p>Live projects you can open and try. The interfaces are in Arabic.</p></div><div class="grid">{work}</div></section>
  <section class="block" id="how"><div class="block-head"><h2>How we work</h2><p>Four stages, each with a clear output you review before the next one.</p></div><ol class="steps">{steps}</ol></section>
  <section class="block" id="faq"><div class="block-head"><h2>FAQ</h2></div><div class="faqs">{faq}</div></section>
  <div class="band" id="contact"><div><h2>Let's start your project</h2><p>Send us a short description of what you need on WhatsApp, and we will reply with a first outline and next steps. Phone: <span class="num">+966 55 791 2466</span></p></div>
    <div class="cta-row"><a class="btn" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Message us on WhatsApp</a><a class="btn ghost" href="tel:+{WA}">Call us</a></div></div>
</main>
<footer class="wrap"><span>© <span class="num" id="year">2026</span> Agentiq · Riyadh, Saudi Arabia</span><span><a href="/" lang="ar">العربية</a> · <a href="/hours/" lang="ar">Savings calculator (Arabic)</a></span></footer>
<a class="fab" href="{wa(msg)}" target="_blank" rel="noopener" aria-label="Message us on WhatsApp">{WA_ICON}<span>WhatsApp</span></a>
<script src="/assets/site.js" defer></script>
</body></html>
'''

def write(rel, text):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(text); print('wrote', rel, len(text))

for sv in SERVICES: write(f'services/{sv["slug"]}/index.html', service_page(sv))
write('en/index.html', en_page())
