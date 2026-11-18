/**
 * Agentiq — calculator leads.
 * Paste into a Google Sheet: Extensions > Apps Script, then Deploy > New deployment > Web app
 * (Execute as: Me, Who has access: Anyone). Put the web app URL in assets/agentiq-config.js.
 *
 * Each "email me the report" request:
 *   1. adds a row to the "العملاء" sheet,
 *   2. emails the visitor their report (built here from the numbers, never from free text),
 *   3. emails you a short notice.
 */
const SHEET_NAME = 'العملاء';
const NOTIFY_OWNER = true;          // set to false to stop the notice emails to you
const DAILY_LIMIT = 80;             // stays under Gmail's daily sending quota
const WHATSAPP = 'https://wa.me/966557912466';

const HEAD = ['التاريخ', 'البريد', 'المجال', 'الموظفون', 'ساعات/أسبوع', 'تكلفة الساعة', 'أخطاء/شهر', 'تكلفة الخطأ',
  'نسبة الأتمتة %', 'تكلفة الأتمتة', 'التكلفة الحالية/شهر', 'بعد الأتمتة/شهر', 'التوفير السنوي', 'ساعات موفّرة/شهر',
  'اللغة', 'الصفحة', 'الحالة', 'ملاحظات'];
const INDUSTRY = { store: 'متجر إلكتروني', clinic: 'عيادة', realty: 'مكتب عقار', food: 'مطعم أو مقهى', services: 'شركة خدمات', custom: 'أرقام مخصصة' };
const INDUSTRY_EN = { store: 'Online store', clinic: 'Clinic', realty: 'Real estate office', food: 'Restaurant or café', services: 'Services company', custom: 'Custom numbers' };

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.website) return ok_();                                   // bots fill the hidden field
  const email = String(p.email || '').trim().toLowerCase().slice(0, 200);
  if (!/^[^\s@=+\-"'<>]+@[^\s@"'<>]+\.[^\s@"'<>]{2,}$/.test(email)) return ok_();

  const cache = CacheService.getScriptCache();
  if (cache.get('e:' + email)) return ok_();                     // same address within the hour
  cache.put('e:' + email, '1', 3600);

  const props = PropertiesService.getScriptProperties();
  const day = Utilities.formatDate(new Date(), 'Asia/Riyadh', 'yyyy-MM-dd');
  const count = props.getProperty('d:' + day) === null ? 0 : +props.getProperty('d:' + day);
  if (count >= DAILY_LIMIT) return ok_();
  props.setProperty('d:' + day, String(count + 1));

  const n = (k, lo, hi) => Math.min(hi, Math.max(lo, Number(p[k]) || 0));
  const v = { emp: n('emp', 1, 50), hrs: n('hrs', 1, 40), rate: n('rate', 20, 300), err: n('err', 0, 100),
              errc: n('errc', 0, 2000), auto: n('auto', 10, 90), inv: n('inv', 3000, 150000) };
  const ind = Object.prototype.hasOwnProperty.call(INDUSTRY, p.industry) ? p.industry : 'custom';
  const en = p.lang === 'en';
  const page = String(p.page || '').slice(0, 40).replace(/^[=+\-@]/, "'");

  const a = v.auto / 100, hoursMonth = v.emp * v.hrs * 4.33;
  const before = hoursMonth * v.rate + v.err * v.errc;
  const after = hoursMonth * (1 - a) * v.rate + v.err * (1 - a) * v.errc;
  const saveMonth = before - after, saveYear = saveMonth * 12, hoursSaved = hoursMonth * a;
  const roi = saveYear / v.inv, payback = saveMonth > 0 ? v.inv / saveMonth : 0;
  const r = Math.round;

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    sheet_().appendRow([new Date(), email, INDUSTRY[ind], v.emp, v.hrs, v.rate, v.err, v.errc, v.auto, v.inv,
      r(before), r(after), r(saveYear), r(hoursSaved), en ? 'EN' : 'AR', page, 'جديد', '']);
  } finally { lock.releaseLock(); }

  const f = (x) => Number(r(x)).toLocaleString('en-US');
  const report = en ? reportEn_(v, INDUSTRY_EN[ind], f, before, after, saveMonth, saveYear, hoursSaved, roi, payback)
                    : reportAr_(v, INDUSTRY[ind], f, before, after, saveMonth, saveYear, hoursSaved, roi, payback);
  MailApp.sendEmail({ to: email, subject: report.subject, htmlBody: report.html, body: report.text, name: 'Agentiq' });

  if (NOTIFY_OWNER) {
    MailApp.sendEmail(Session.getEffectiveUser().getEmail(),
      'عميل جديد من الحاسبة: ' + email,
      INDUSTRY[ind] + ' · توفير سنوي ' + f(saveYear) + ' ر.س\n' + SpreadsheetApp.getActive().getUrl());
  }
  return ok_();
}

function doGet() { return ok_(); }

function ok_() { return ContentService.createTextOutput('{"ok":true}').setMimeType(ContentService.MimeType.JSON); }

function sheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEAD);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEAD.length).setFontWeight('bold').setBackground('#ECEBFF');
    sh.setRightToLeft(true);
    sh.getRange('A:A').setNumberFormat('yyyy-mm-dd hh:mm');
    sh.getRange('Q2:Q').setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(['جديد', 'تم التواصل', 'استشارة محجوزة', 'عميل', 'غير مهتم'], true).build());
  }
  return sh;
}

function reportAr_(v, ind, f, before, after, saveMonth, saveYear, hoursSaved, roi, payback) {
  const rows = [
    ['المجال', ind],
    ['الشغل المتكرر', v.emp + ' موظف × ' + v.hrs + ' ساعة أسبوعياً، تكلفة الساعة ' + v.rate + ' ر.س'],
    ['الأخطاء', v.err + ' خطأ شهرياً بتكلفة ' + f(v.errc) + ' ر.س للخطأ'],
    ['التكلفة الحالية', f(before) + ' ر.س شهرياً'],
    ['بعد أتمتة ' + v.auto + '%', f(after) + ' ر.س شهرياً'],
    ['ساعات توفّرها', f(hoursSaved) + ' ساعة شهرياً'],
    ['العائد', 'كل ريال يرجع ' + roi.toFixed(1) + ' ريال خلال سنة · تسترد التكلفة في ' + (payback < 1 ? 'أقل من شهر' : payback.toFixed(1) + ' شهر')],
  ];
  const html = '<div dir="rtl" style="font-family:Tahoma,Arial,sans-serif;color:#1A1B2E;max-width:560px">'
    + '<p style="font-size:15px">هذا تقرير تكلفة الشغل اليدوي اللي طلبته من حاسبة Agentiq.</p>'
    + '<div style="background:linear-gradient(120deg,#00A890,#5B4BFF);color:#fff;border-radius:14px;padding:18px 20px;margin:14px 0">'
    + '<div style="font-size:14px">التوفير السنوي المتوقع</div><div style="font-size:30px;font-weight:bold">' + f(saveYear) + ' ر.س</div>'
    + '<div style="font-size:14px">يعني ' + f(saveMonth) + ' ر.س كل شهر</div></div>'
    + '<table style="width:100%;border-collapse:collapse;font-size:14px">'
    + rows.map((x) => '<tr><td style="padding:8px;border-bottom:1px solid #E6E8F2;color:#6B7090;width:38%">' + x[0] + '</td><td style="padding:8px;border-bottom:1px solid #E6E8F2">' + x[1] + '</td></tr>').join('')
    + '</table><p style="font-size:13px;color:#6B7090">أرقام تقديرية ومتحفّظة. النتيجة الفعلية نحسبها معك في الاستشارة.</p>'
    + '<p><a href="' + WHATSAPP + '" style="display:inline-block;background:#5B4BFF;color:#fff;text-decoration:none;padding:11px 18px;border-radius:10px;font-weight:bold">احجز استشارة مجانية</a></p>'
    + '<p style="font-size:13px;color:#6B7090">Agentiq · https://sarahalolayan.github.io</p></div>';
  const text = 'تقرير تكلفة الشغل اليدوي (Agentiq)\nالتوفير السنوي المتوقع: ' + f(saveYear) + ' ر.س\n'
    + rows.map((x) => x[0] + ': ' + x[1]).join('\n') + '\n\nللاستشارة المجانية: ' + WHATSAPP;
  return { subject: 'تقريرك: توفير متوقع ' + f(saveYear) + ' ر.س بالسنة', html: html, text: text };
}

function reportEn_(v, ind, f, before, after, saveMonth, saveYear, hoursSaved, roi, payback) {
  const rows = [
    ['Industry', ind],
    ['Repetitive work', v.emp + ' staff × ' + v.hrs + ' h/week, SAR ' + v.rate + ' per hour'],
    ['Errors', v.err + ' per month at SAR ' + f(v.errc) + ' each'],
    ['Current cost', 'SAR ' + f(before) + ' / month'],
    ['After ' + v.auto + '% automation', 'SAR ' + f(after) + ' / month'],
    ['Hours saved', f(hoursSaved) + ' h / month'],
    ['Return', 'Every riyal returns ' + roi.toFixed(1) + ' in a year · pays back in ' + (payback < 1 ? 'under a month' : payback.toFixed(1) + ' months')],
  ];
  const html = '<div style="font-family:Arial,sans-serif;color:#1A1B2E;max-width:560px">'
    + '<p style="font-size:15px">Here is the manual work cost report you requested from the Agentiq calculator.</p>'
    + '<div style="background:linear-gradient(120deg,#00A890,#5B4BFF);color:#fff;border-radius:14px;padding:18px 20px;margin:14px 0">'
    + '<div style="font-size:14px">Expected yearly savings</div><div style="font-size:30px;font-weight:bold">SAR ' + f(saveYear) + '</div>'
    + '<div style="font-size:14px">That is SAR ' + f(saveMonth) + ' every month</div></div>'
    + '<table style="width:100%;border-collapse:collapse;font-size:14px">'
    + rows.map((x) => '<tr><td style="padding:8px;border-bottom:1px solid #E6E8F2;color:#6B7090;width:38%">' + x[0] + '</td><td style="padding:8px;border-bottom:1px solid #E6E8F2">' + x[1] + '</td></tr>').join('')
    + '</table><p style="font-size:13px;color:#6B7090">Conservative estimates. We work out the real figure with you in the consultation.</p>'
    + '<p><a href="' + WHATSAPP + '" style="display:inline-block;background:#5B4BFF;color:#fff;text-decoration:none;padding:11px 18px;border-radius:10px;font-weight:bold">Book a free consultation</a></p>'
    + '<p style="font-size:13px;color:#6B7090">Agentiq · https://sarahalolayan.github.io/en/</p></div>';
  const text = 'Manual work cost report (Agentiq)\nExpected yearly savings: SAR ' + f(saveYear) + '\n'
    + rows.map((x) => x[0] + ': ' + x[1]).join('\n') + '\n\nFree consultation: ' + WHATSAPP;
  return { subject: 'Your report: SAR ' + f(saveYear) + ' expected yearly savings', html: html, text: text };
}
