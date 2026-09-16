// POST /api/apply — a clinic account application.
//
// Ordering is not open yet but accounts are: a practice applies now and has its
// pricing tier set and waiting for the day the shop opens.

const { clean, validEmail, validAbn, needList, send, guard } = require('./_lib.js');

module.exports = async function handler(req, res) {
  const body = guard(req, res);
  if (!body) return;

  const practice = clean(body.practice, 120);
  const abn = clean(body.abn, 20);
  const contact = clean(body.contact, 100);
  const email = clean(body.email, 160);
  const note = clean(body.note, 1200);

  const problems = [];
  if (!practice) problems.push('a practice name');
  if (!contact) problems.push('a contact name');
  if (!validEmail(email)) problems.push('a valid work email');
  if (!validAbn(abn)) problems.push('a valid 11 digit ABN');
  if (problems.length) return res.status(400).json({ ok: false, message: needList(problems) });

  const r = await send({
    subject: `Clinic application: ${practice}`,
    replyTo: email,
    rows: [['Practice', practice], ['ABN', abn], ['Contact', contact],
           ['Work email', email], ['Note', note || '(none)']],
  });
  return r.status === 200
    ? res.status(200).json({ ok: true })
    : res.status(r.status).json({ ok: false, message: r.message });
};
