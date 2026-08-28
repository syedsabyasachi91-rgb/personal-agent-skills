$ErrorActionPreference = 'Stop'
$dir = Join-Path $PSScriptRoot 'fixtures'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$out = Join-Path $dir 'api-doc-large.md'

$lines = @(
    '# Payments API Documentation'
    ''
    '## Overview'
    'Base URL: https://api.example.com/v1'
    'All requests require JSON bodies. Responses are JSON.'
    ''
)

$i = 0
foreach ($ep in @('charges', 'refunds', 'customers', 'disputes')) {
    foreach ($verb in @('GET', 'POST', 'PUT', 'DELETE')) {
        $i++
        $lines += "### $verb /v1/$ep/$i"
        $lines += "Standard $verb operation for $ep resource #$i."
        $lines += 'Request body: { "amount": integer, "currency": string }'
        $lines += ''
    }
}
while ($lines.Count -lt 560) {
    $lines += "Reference note $($lines.Count): pagination cursors paginate through collections."
}

$lines += '## Authentication'
$lines += 'All endpoints require a Bearer token in the Authorization header.'
$lines += 'Tokens are obtained via POST /v1/auth/token with client_id and client_secret.'
$lines += 'Tokens expire after 3600 seconds; refresh via POST /v1/auth/refresh.'
$lines += ''

while ($lines.Count -lt 800) {
    $lines += "Filler line $($lines.Count): see the charges endpoint for typical usage."
}

$lines += '## Error Codes'
$lines += '- 400 invalid_request: malformed body'
$lines += '- 401 unauthorized: missing or expired token'
$lines += '- 402 card_declined: issuer refused charge'
$lines += '- 429 rate_limited: too many requests'
$lines += ''
$lines += '## Rate Limits'
$lines += '100 requests per minute per key. On 429, retry after the Retry-After header value.'
$lines += ''
$lines += '## Versioning'
$lines += 'API version pinned via the X-API-Version header. Breaking changes ship as new dates.'

Set-Content -LiteralPath $out -Value $lines -Encoding UTF8
$count = (Get-Content -LiteralPath $out).Count
Write-Output "Fixture written: $out ($count lines)"
