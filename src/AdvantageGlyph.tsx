import { MapPin, type LucideIcon } from 'lucide-react';

export interface DisplayAdvantage {
  title: string;
  description?: string;
  icon_type: 'fa' | 'svg' | 'lucide';
  fa_icon?: string | null;
  svg_url?: string | null;
  lucide?: LucideIcon;
}

interface Props {
  adv: DisplayAdvantage;
  size?: number;
  className?: string;
  iconClassName?: string;
}

/**
 * Renders an advantage icon for any of the three backend-supported types:
 * - lucide (fallback / hardcoded demo data)
 * - fa     (Font Awesome / Remix class from the admin panel)
 * - svg    (uploaded SVG file from the admin panel)
 */
export default function AdvantageGlyph({ adv, size = 28, className, iconClassName }: Props) {
  if (adv.icon_type === 'svg' && adv.svg_url) {
    return (
      <img
        src={adv.svg_url}
        alt=""
        width={size}
        height={size}
        className={`object-contain ${className ?? ''}`}
        style={{ width: size, height: size }}
      />
    );
  }

  if (adv.icon_type === 'fa' && adv.fa_icon) {
    return (
      <i
        className={`${adv.fa_icon} ${iconClassName ?? ''}`}
        style={{ fontSize: size }}
        aria-hidden="true"
      />
    );
  }

  const Icon = adv.lucide ?? MapPin;
  return <Icon className={className} style={{ width: size, height: size }} />;
}
