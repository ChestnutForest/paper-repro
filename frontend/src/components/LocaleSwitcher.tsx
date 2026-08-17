import { useRouter } from 'next/router'
import { useTranslations } from 'next-intl'

export function LocaleSwitcher() {
  const router = useRouter()
  const t = useTranslations('locale_switcher')

  const changeLocale = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const locale = e.target.value
    router.push(router.pathname, router.asPath, { locale })
  }

  return (
    <div className="z-50">
      <select
        value={router.locale}
        onChange={changeLocale}
        className="text-sm bg-transparent border border-muted rounded px-2 py-1 outline-none focus:ring-1 focus:ring-primary cursor-pointer hover:bg-muted/30 transition-colors"
      >
        <option value="ja">{t('ja')}</option>
        <option value="en">{t('en')}</option>
        <option value="zh-TW">{t('zh-TW')}</option>
      </select>
    </div>
  )
}
